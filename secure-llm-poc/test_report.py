# test_report.py

import json
import csv
from collections import Counter

LOG_FILE = "logs/interaction_log.json"
CSV_FILE = "logs/test_report_summary.csv"
JSON_EXPORT_FILE = "logs/test_report_full.json"

def analyze_logs():
    verdicts = []
    total = 0
    full_data = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            full_data.append(entry)
            verdict = entry.get("verdict", "unknown")
            verdicts.append(verdict)
            total += 1

    stats = Counter(verdicts)

    print("\n--- Rapport d'évaluation ---")
    print(f"Total de prompts testés : {total}\n")
    for verdict, count in stats.items():
        pct = (count / total) * 100
        print(f"{verdict:<20} : {count} ({pct:.1f}%)")

    # Export CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Verdict", "Nombre", "Pourcentage"])
        for verdict, count in stats.items():
            pct = (count / total) * 100
            writer.writerow([verdict, count, f"{pct:.1f}%"])

    print(f"\nRapport CSV sauvegardé dans : {CSV_FILE}")

    # Export JSON complet
    with open(JSON_EXPORT_FILE, "w", encoding="utf-8") as jsonfile:
        json.dump(full_data, jsonfile, indent=2, ensure_ascii=False)

    print(f"Export JSON complet sauvegardé dans : {JSON_EXPORT_FILE}")

if __name__ == "__main__":
    analyze_logs()
