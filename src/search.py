from Bio import Entrez

Entrez.email = "randolphl@uthscsa.edu"

def run_search(search_term):
    handle = Entrez.esearch(
        db="gds",
        term=search_term,
        retmax=500,
        datetype="pdat",
        reldate=7   # last 7 days
    )
    record = Entrez.read(handle)
    handle.close()

    gse_ids = record["IdList"]

    # Fetch summaries
    handle = Entrez.esummary(db="gds", id=",".join(gse_ids))
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
