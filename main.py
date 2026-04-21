# orchestrates workflow

import yaml
import csv
from src.search import run_search
from src.storage import load_seen_ids, save_seen_ids

OUTPUT_PATH = "outputs/weekly_report.csv"


def save_report(rows):
    import os
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["GSE_ID", "LINK", "STATUS"])

        for r in rows:
            writer.writerow(r)


def main():
    with open("configs/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    print("🔄 Running GEO search...")

    # CURRENT 730-DAY RESULTS (your “new window”)
    current_ids = set(run_search(config["weekly_search"], config["email"]))

    # FULL HISTORICAL MEMORY
    seen_ids = load_seen_ids()

    # update archive (keeps everything ever seen)
    all_ids = seen_ids.union(current_ids)
    save_seen_ids(all_ids)

    # -----------------------
    # BUILD LABELED REPORT
    # -----------------------
    rows = []

    for gse in all_ids:
        status = "new" if gse in current_ids else "old"

        rows.append((
            gse,
            f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}",
            status
        ))

    save_report(rows)

    # -----------------------
    # SUMMARY
    # -----------------------
    new_ids = current_ids - seen_ids

    print("\n✔ Pipeline complete")
    print(f"Total studies tracked: {len(all_ids)}")
    print(f"New studies this run: {len(new_ids)}")

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")


if __name__ == "__main__":
    main()
