import os
import csv

REPORT_PATH = "outputs/weekly_report.csv"

def append_to_weekly_report(new_ids):
  os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
  
  file_exists = os.path.isfile(REPORT_PATH)
  
  with open(REPORT_PATH, "a", newline="") as f:
    writer = csv.writer(f)
    
    # Writer header only if file doesn't exist yet
    if not file_exists:
      writer.writerow(["GSE_ID", "Link"])
      
    for gse_id in new_ids:
        link = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse_id}"
        writer.writerow([gse_id, link])
