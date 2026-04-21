import os

FILE_PATH = "data/gse_ids.csv"

def load_seen_ids():
    if not os.path.exists(FILE_PATH):
        return set()

    with open(FILE_PATH, "r") as f:
        return set(line.strip() for line in f)


def save_seen_ids(new_ids):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    existing_ids = load_seen_ids()

    with open(FILE_PATH, "a") as f:
        for i in new_ids:
            if i not in existing_ids:
                f.write(f"{i}\n")
                existing_ids.add(i)
