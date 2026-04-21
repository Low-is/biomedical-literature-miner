# orchestrates workflow

import yaml
from src.search import run_search
from src.storage import load_seen_ids, save_seen_ids
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

    current_ids = set(run_search(config))  # ensure set for safe ops
    seen_ids = load_seen_ids()

    # -----------------------
    # COMPUTE STATE
    # -----------------------
    new_ids = current_ids - seen_ids
    all_ids = seen_ids.union(current_ids)

    # -----------------------
    # REPORT (CURRENT RUN ONLY)
    # -----------------------
    append_to_weekly_report(current_ids)

    print(f"Found {len(new_ids)} NEW datasets:\n")

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")

    # -----------------------
    # SAVE STATE (FULL HISTORY)
    # -----------------------
    save_seen_ids(all_ids)

if __name__ == "__main__":
    main()
