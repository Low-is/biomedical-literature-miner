# orchestrates workflow

import yaml
import csv
from src.search import run_search

OUTPUT_PATH = "outputs/weekly_report.csv"


def save_report(rows):
    import os
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["GSE_ID", "LINK", "STATUS"])
        writer.writerows(rows)


def main():
    with open("configs/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    print("🔍 Running GEO searches...")

    # -----------------------
    # GET ALL DATA (NO STATE, NO FILTERING)
    # -----------------------
    archive_ids = set(run_search(config["archive_search"], config["email"]))
    recent_ids = set(run_search(config["weekly_search"], config["email"]))

    # UNION = ALL STUDIES YOU FOUND
    all_ids = archive_ids.union(recent_ids)

    # -----------------------
    # BUILD REPORT
    # -----------------------
    rows = []

    for gse in all_ids:
        status = "new" if gse in recent_ids else "old"

        rows.append((
            gse,
            f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}",
            status
        ))

    save_report(rows)

    print("\n✔ Pipeline complete")
    print(f"Total studies: {len(rows)}")
    print(f"New (last 730 days): {len(recent_ids)}")
    print(f"Old (archive-only): {len(archive_ids - recent_ids)}")


if __name__ == "__main__":
    main()
