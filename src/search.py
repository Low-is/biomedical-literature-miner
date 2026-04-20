from Bio import Entrez

Entrez.email = "randolphl@uthscsa.edu"

def run_search(search_term):
    search_cfg = config["search"]
    
    handle = Entrez.esearch(
        db=search_cfg["database"],
        term=search_cfg["query"],
        retmax=search_cfg["retmax"],
        datetype="pdat",
        reldate=search_cfg["reldate"]
    )
    record = Entrez.read(handle)
    handle.close()

    gse_ids = record["IdList"]

    # Fetch summaries
    handle = Entrez.esummary(
        db=search_cfg["database"],
        id=",".join(gse_ids)
    )
    summaries = Entrez.read(handle)
    handle.close()

    gse_list = []

    if isinstance(summaries, dict) and "DocumentSummarySet" in summaries:
        docs = summaries["DocumentSummarySet"]["DocumentSummary"]
    else:
        docs = summaries

    for doc in docs:
        acc = doc.get("Accession", "")
        if acc.startswith("GSE"):
            gse_list.append(acc)

    return gse_list
