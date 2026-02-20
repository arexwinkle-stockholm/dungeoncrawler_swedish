import json

# Input and output file paths
input_file = "anya_fixed.json"
output_file = "anya_single_line.json"

# Read the formatted JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Write JSON in single-line (compact) format
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

print("Conversion complete. JSON is now on a single line.")