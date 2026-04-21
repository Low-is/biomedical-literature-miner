# orchestrates workflow

import yaml
from src.search import run_search
from src.storage import load_seen_ids, save_seen_ids
from src.report_writer import append_to_weekly_report

def run_archive_pipeline(config):
    print("📚 Building historical GEO archive...")
    archive_ids = set(run_search(config["archive_search"]))

    # Save full archive snapshot (optional separate file if you want)
    append_to_weekly_report(archive_ids)

    print(f"Archive size: {len(archive_ids)} datasets collected\n")


def run_weekly_pipeline(config):
    print("🔄 Running weekly GEO surveillance...")

    current_ids = set(run_search(config["weekly_search"]))
    seen_ids = load_seen_ids()

    new_ids = current_ids - seen_ids
    all_ids = seen_ids.union(current_ids)

    append_to_weekly_report(current_ids)

    print(f"Found {len(new_ids)} NEW datasets:\n")

    for gse in new_ids:
        print(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")

    save_seen_ids(all_ids)


def main():
    with open("configs/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # -----------------------
    # RUN BOTH MODES
    # -----------------------
    run_archive_pipeline(config)
    run_weekly_pipeline(config)


if __name__ == "__main__":
    main()
