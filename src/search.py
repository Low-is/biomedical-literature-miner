import re
from Bio import Entrez


def normalize(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------------------------------
# BIOLOGICAL FILTER ONLY (NO PLATFORM LOGIC HERE)
# -------------------------------------------------
def keep_study(study):

    text = normalize(
        study.get("title", "")
    )

    # Must be sepsis
    if "sepsis" in text:
        return True


# -------------------------------------------------
# PLATFORM FILTER (DNA vs RNA)
# -------------------------------------------------
def is_correct_platform(study, search_cfg):

    text = normalize(
        study.get("title", "") + " " +
        study.get("summary", "") + " " +
        study.get("type", "")
    )

    query = search_cfg["query"].lower()

    # ---------------- DNA MICROARRAY ----------------
    if "microarray" in text or "expression profiling by array" in text:
        return True
        
        if "methylation" in text or "genome tiling" in text:
            return False

        return True

    # ---------------- RNA-seq ----------------
    else:

        if "other" in text:
            return False

        return True


# -------------------------------------------------
# MAIN SEARCH FUNCTION
# -------------------------------------------------
def run_search(search_cfg, email):

    Entrez.email = email

    esearch_params = {
        "db": search_cfg["database"],
        "term": search_cfg["query"],
        "retmax": search_cfg["retmax"],
    }

    if "reldate" in search_cfg:
        esearch_params["reldate"] = search_cfg["reldate"]
        esearch_params["datetype"] = "pdat"

    handle = Entrez.esearch(**esearch_params)
    record = Entrez.read(handle)
    handle.close()

    gse_ids = record.get("IdList", [])

    if not gse_ids:
        return []

    handle = Entrez.esummary(
        db=search_cfg["database"],
        id=",".join(gse_ids)
    )

    summaries = Entrez.read(handle)
    handle.close()

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

        # STEP 1: PLATFORM FILTER
        if not is_correct_platform(study, search_cfg):
            continue

        # STEP 2: BIOLOGICAL FILTER
        if not keep_study(study):
            continue

        gse_list.append(study)

    return gse_list


with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
archive_dna = run_search(config["dna_archive_search"], config["email"])
print(archive_dna)
