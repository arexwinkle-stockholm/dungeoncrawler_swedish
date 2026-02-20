import json
import re
from collections import defaultdict


INPUT_FILE = "all_chapters_raw.json"
OUTPUT_FILE = "all_chapters_clean.json"


def is_phrase(text):
    text = text.strip()
    if re.search(r"[.!?]$", text):
        return True
    if len(text.split()) > 1 and not re.search(r"\(.*?\)", text):
        return True
    return False


def build_form(base, form):
    form = form.strip()

    if form in ["–", "-", ""]:
        return None

    if form.startswith("-"):
        return base + form[1:]

    return form


def parse_parentheses(entry):
    match = re.match(r"^(.*?)\s*\((.*?)\)$", entry)
    if not match:
        return None, None

    base = match.group(1).strip()
    forms_raw = [f.strip() for f in match.group(2).split(",")]

    return base, forms_raw


def clean_flashcards(data):
    cleaned = []
    chapter_counters = defaultdict(int)

    for card in data:
        front_original = card["front"].strip()
        back_clean = re.sub(r"[.!?]$", "", card["back"].strip())
        chapter_name = card.get("chapter", "Unknown")

        chapter_counters[chapter_name] += 1
        chapter_prefix = chapter_name.lower().replace(" ", "")
        entry_id = f"{chapter_prefix}_{str(chapter_counters[chapter_name]).zfill(3)}"

        new_entry = {
            "id": entry_id,
            "chapter": chapter_name,
            "difficulty": 1,
            "tags": []
        }

        # Phrase
        if is_phrase(front_original):
            new_entry.update({
                "type": "phrase",
                "front": front_original,
                "back": back_clean
            })
            cleaned.append(new_entry)
            continue

        # Word with forms
        base, forms_raw = parse_parentheses(front_original)

        if base and forms_raw:
            new_entry.update({
                "type": "word",
                "partOfSpeech": "unknown",
                "front": base,
                "back": back_clean
            })

            if len(forms_raw) == 3:
                new_entry["forms"] = {
                    "form1": build_form(base, forms_raw[0]),
                    "form2": build_form(base, forms_raw[1]),
                    "form3": build_form(base, forms_raw[2])
                }
            else:
                new_entry["forms"] = {
                    "raw": forms_raw
                }

            cleaned.append(new_entry)
            continue

        # Simple word
        new_entry.update({
            "type": "word",
            "partOfSpeech": "unknown",
            "front": front_original,
            "back": back_clean,
            "forms": None
        })

        cleaned.append(new_entry)

    return cleaned


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = clean_flashcards(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Processed {len(cleaned_data)} entries.")
    print(f"Clean file written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()