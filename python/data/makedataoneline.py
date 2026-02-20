import json

INPUT_FILE = "datalibrary.json"
OUTPUT_FILE = "21chaptersoneline.json"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Write JSON as a single line
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Minified JSON written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()