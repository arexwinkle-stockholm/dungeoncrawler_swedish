import csv
import json

cards = []

with open("vocab.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cards.append({
            "front": row["Front"],
            "back": row["Back"]
        })

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Flashcards</title>
<style>
  body {{
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 50px;
    background-color: #000;
    color: #fff;
  }}
  #card {{
    border: 1px solid #555;
    padding: 40px;
    width: 350px;
    margin: 20px auto;
    font-size: 24px;
    cursor: pointer;
    user-select: none;
    background-color: #111;
    border-radius: 8px;
  }}
  .controls {{
    margin-bottom: 20px;
  }}
  button {{
    font-size: 22px;
    margin: 0 10px;
    cursor: pointer;
    background-color: #222;
    color: #fff;
    border: 1px solid #555;
    padding: 10px 16px;
    border-radius: 6px;
  }}
  button:hover {{
    background-color: #333;
  }}
</style>
</head>
<body>

<h2>Flashcards</h2>

<div class="controls">
  <button onclick="prevCard()">⬅️</button>
  <button onclick="nextCard()">➡️</button>
  <button onclick="randomize()">🔀 Randomize</button>
</div>

<div id="card"></div>

<script>
let cards = {json.dumps(cards)};
let index = 0;
let flipped = false;

const cardDiv = document.getElementById("card");

function render() {{
  cardDiv.innerText = flipped ? cards[index].back : cards[index].front;
}}

function nextCard() {{
  index = (index + 1) % cards.length;
  flipped = false;
  render();
}}

function prevCard() {{
  index = (index - 1 + cards.length) % cards.length;
  flipped = false;
  render();
}}

function randomize() {{
  for (let i = cards.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }}
  index = 0;
  flipped = false;
  render();
}}

cardDiv.onclick = function() {{
  flipped = !flipped;
  render();
}}

render();
</script>

</body>
</html>
"""

with open("flashcards.html", "w", encoding="utf-8") as f:
    f.write(html)

print("flashcards.html created!")
