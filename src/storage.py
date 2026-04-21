import os

FILE_PATH = "data/gse_ids.csv"

def load_seen_ids():
    if not os.path.exists(FILE_PATH):
        return set()

    with open(FILE_PATH, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_seen_ids(all_ids):
    """
    This file ALWAYS represents full history:
    2014 → present (no duplicates ever)
    """

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    # overwrite file with deduplicated full history
    with open(FILE_PATH, "w") as f:
        for i in sorted(all_ids):
            f.write(f"{i}\n")
