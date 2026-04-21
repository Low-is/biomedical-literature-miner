# orchestrates workflow

import yaml
from src.search import run_search
from src.storage import load_seen_ids, save_seen_ids
from src.filter import get_new_ids
from src.report_writer import append_to_weekly_report

def main():
    # -----------------------
    # LOAD CONFIG
    # -----------------------
    with open("configs/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # -----------------------
    # RUN SEARCH
    # -----------------------
    print("🔍 Running weekly GEO search...")

    current_ids = run_search(config)
    
    seen_ids = load_seen_ids()
    new_ids = get_new_ids(current_ids, seen_ids)

    print(f"Found {len(new_ids)} NEW datasets:\n")

    # -----------------------
    # SAVE REPORT
    # -----------------------
    append_to_weekly_report(current_ids)
    

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")

    # -----------------------
    # SAVE STATE
    # -----------------------
    all_ids = set(current_ids).union(seen_ids)
    save_seen_ids(current_ids)

if __name__ == "__main__":
    main()
