import json
from collections import defaultdict

# Load JSON data from file
with open("anya_single_line.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Dictionary to store counts per chapter
chapter_counts = defaultdict(int)

# Count entries per chapter
for entry in data:

    # If entry is a list (nested structure)
    if isinstance(entry, list):
        for item in entry:
            if isinstance(item, dict):
                chapter = item.get("chapter", "").strip()
                if chapter:
                    chapter_counts[chapter] += 1

    # If entry is already a dictionary (flat structure)
    elif isinstance(entry, dict):
        chapter = entry.get("chapter", "").strip()
        if chapter:
            chapter_counts[chapter] += 1

# Print results for Chapter1 to Chapter24 (even if zero)
for i in range(1, 25):  # 1 through 24
    chapter_name = f"Chapter{i}"
    count = chapter_counts.get(chapter_name, 0)
    print(f"{chapter_name}: {count} items")

# Optional: total count
total = sum(chapter_counts.values())
print(f"\nTotal entries: {total}")