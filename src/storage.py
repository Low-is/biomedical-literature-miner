import os

FILE_PATH = "data/gse_ids.csv"

def load_seen_ids():
    if not os.path.exists(FILE_PATH):
        return set()

    with open(FILE_PATH, "r") as f:
        return set(line.strip() for line in f)

def save_seen_ids(ids):
    with open(FILE_PATH, "w") as f:
        for i in ids:
            f.write(f"{i}\n")
