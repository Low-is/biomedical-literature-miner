# orchestrates workflow

from src.search import run_search
from src.storage import load_seen_ids, save_seen_ids
from src.filter import get_new_ids

def main():
    search_term = (
        '(bronchopulmonary dysplasia OR BPD) AND '
        '(RNA-seq OR RNAseq OR microarray OR "gene expression profiling") AND '
        '(Homo sapiens[Organism]) AND '
        '(neonate OR newborn OR infant OR preterm)'
    )

    print("🔍 Running weekly GEO search...")

    current_ids = run_search(search_term)
    seen_ids = load_seen_ids()

    new_ids = get_new_ids(current_ids, seen_ids)

    print(f"Found {len(new_ids)} NEW datasets:\n")

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")

    # Update stored IDs
    all_ids = set(current_ids).union(seen_ids)
    save_seen_ids(all_ids)

if __name__ == "__main__":
    main()
