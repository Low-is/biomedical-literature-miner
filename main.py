# orchestrates workflow

import yaml
from src.search import run_search
from src.storage import load_seen_ids, save_seen_ids, save_weekly_report


def run_archive_pipeline(config):
    print("📚 Building historical GEO archive...")

    archive_ids = set(run_search(config["archive_search"], config["email"]))

    print(f"Archive size: {len(archive_ids)} datasets collected\n")

    return archive_ids


def run_weekly_pipeline(config):
    print("🔄 Running weekly GEO surveillance...")

    current_ids = set(run_search(config["weekly_search"], config["email"]))
    seen_ids = load_seen_ids()

    new_ids = current_ids - seen_ids
    old_ids = current_ids & seen_ids

    all_ids = seen_ids.union(current_ids)

    # -----------------------
    # BUILD LABELED ROWS
    # -----------------------
    rows = []

    for gse in new_ids:
        rows.append((
            gse,
            f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}",
            "new"
        ))

    for gse in old_ids:
        rows.append((
            gse,
            f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}",
            "existing"
        ))

    # -----------------------
    # SAVE STATE + REPORT
    # -----------------------
    save_seen_ids(all_ids)
    save_weekly_report(rows)

    print(f"Found {len(new_ids)} NEW datasets:\n")

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")

    return current_ids


def main():
    with open("configs/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    archive_ids = run_archive_pipeline(config)
    weekly_ids = run_weekly_pipeline(config)

    final_ids = archive_ids.union(weekly_ids)
    seen_ids = load_seen_ids()

    new_ids = final_ids - seen_ids

    print("\n✔ Pipeline complete")
    print(f"Total archive size: {len(final_ids)}")
    print(f"New datasets this run: {len(new_ids)}")

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")


if __name__ == "__main__":
    main()
