import re
from Bio import Entrez


def normalize(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
    

def keep_study(study):

    text = normalize(
        study.get("title", "") + " " +
        study.get("summary", "") + " " +
        study.get("type", "")
    )

    # Disease
    if "sepsis" not in text:
        return False

    # Neonatal terms
    neonatal_terms = [
        "neonate",
        "newborn",
        "infant",
        "preterm",
        "premature",
        "extremely low gestational age",
    ]

    if not any(term in text for term in neonatal_terms):
        return False

    # Exclude unwanted studies
    exclude_terms = [
        "methylation",
        "bisulfite",
        "single cell",
        "single-cell",
        "scrna",
        "scrna seq",
        "snrna",
        "single nucleus",
        "10x",
        "cell ranger",
        "cellranger",
        "spatial",
    ]

    if any(term in text for term in exclude_terms):
        return False

    return True
    

def run_search(search_cfg, email):

    Entrez.email = email

    # -------------------------
    # BUILD SEARCH PARAMETERS
    # -------------------------
    esearch_params = {
        "db": search_cfg["database"],
        "term": search_cfg["query"],
        "retmax": search_cfg["retmax"],
    }

    # ONLY ADD reldate IF IT EXISTS
    if "reldate" in search_cfg:
        esearch_params["reldate"] = search_cfg["reldate"]
        esearch_params["datetype"] = "pdat"

    # -------------------------
    # SEARCH GEO DATASETS
    # -------------------------
    handle = Entrez.esearch(**esearch_params)
    record = Entrez.read(handle)
    handle.close()

    gse_ids = record.get("IdList", [])

    if not gse_ids:
        return []

    # -------------------------
    # FETCH SUMMARIES
    # -------------------------
    handle = Entrez.esummary(
        db=search_cfg["database"],
        id=",".join(gse_ids)
    )

    summaries = Entrez.read(handle)
    handle.close()

    # -------------------------
    # PARSE RESULTS
    # -------------------------
    
    # Made changes 7-1-2026
    if isinstance(summaries, list):
        docs = summaries
    else:
        docs = summaries.get("DocumentSummarySet", {}).get("DocumentSummary", [])

    gse_list = []
    
    for doc in docs:
        acc = doc.get("Accession", "") or doc.get("accession", "")
        
        if not str(acc).startswith("GSE"):
            continue

        study = {
            "gse": acc,
            "title": doc.get("title", "") or doc.get("Title", ""),
            "summary": doc.get("summary", "") or doc.get("Summary", ""),
            "type": doc.get("type", "") or doc.get("Type", ""),
            "overall_design": doc.get("overall_design", "") or doc.get("Overall_Design", "")
        }

        text = normalize(
            study.get("title", "") + " " +
            study.get("summary", "") + " " +
            study.get("type", "")
        )

        query = search_cfg["query"].lower()

        if "expression profiling by array" in query or "microarray" in query:

            dna_terms = [
                "expression profiling by array",
                "microarray",
                "gene expression profiling",
                "affymetrix",
                "agilent"
            ]

            if not any(term in text for term in dna_terms):
                continue

        else:

            rna_terms = [
                "expression profiling by high throughput sequencing",
                "rna seq",
                "rna sequencing",
                "rnaseq"
            ]

            if not any(term in text for term in rna_terms):
                continue

        if keep_study(study):
            gse_list.append(study)

    return gse_list

        #gse_list.append({
            #"gse": acc,
            #"title": doc.get("title", "") or doc.get("Title", ""),
            #"summary": doc.get("summary", "") or doc.get("Summary", ""),
            #"type": doc.get("type", "") or doc.get("Type", ""),
            #"overall_design": doc.get("overall_design", "") or doc.get("Overall_Design", "")
        #})

    #return gse_list
