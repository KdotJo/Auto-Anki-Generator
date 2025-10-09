import pypdf, sys, textwrap, os, genanki, re
from openai import OpenAI
from pathlib import Path


client = OpenAI()

if not client.api_key:
    sys.exit("ERROR: OPENAI_API_KEY not found in environment variables.")

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

prompt = Path("prompt.txt").read_text(encoding="utf-8")

def summarize(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",   "content": f"Lecture notes:\n{text[:5000]}"}
        ],
        temperature=0.25
    )
    return response.choices[0].message.content.strip()

MODEL_ID  = 1_607_392_319   
DECK_ID   = 2_059_400_110   

MODEL = genanki.Model(
    MODEL_ID,
    'Auto-Bullet Model',
    fields=[{'name': 'Q'}, {'name': 'A'}],
    templates=[
        {'name': 'Forward', 'qfmt': '{{Q}}', 'afmt': '{{Q}}<hr>{{A}}'},
        {'name': 'Reverse', 'qfmt': '{{A}}', 'afmt': '{{A}}<hr>{{Q}}'}
    ]
)

def _qa(bullets: str) -> list[tuple[str, str]]:
    """
    Return list of (question, answer) pairs.
    **Heading** → question
    everything underneath (indented lines starting with '-') → answer
    """
    cards = []
    current_q = None
    answer_lines = []

    for line in bullets.splitlines():
        line = line.rstrip()
        if not line:
            continue

        # new major heading
        if line.startswith('• '):
            # flush previous card
            if current_q is not None:
                cards.append((current_q, '\n'.join(answer_lines)))
            # start new card
            current_q = line[2:].strip()
            answer_lines = []
            continue

        # indented bullet belonging to current heading
        if line.startswith('  - ') and current_q is not None:
            answer_lines.append(line[4:].strip() + '<br>' + '<br>')
            continue

    # don't forget last card
    if current_q is not None:
        cards.append((current_q, '\n'.join(answer_lines)))
    return cards

def build_deck(bullets: str, outfile: str = 'lecture.apkg'):
    deck = genanki.Deck(DECK_ID, 'Lecture Deck')
    for q, a in _qa(bullets):
        deck.add_note(genanki.Note(model=MODEL, fields=[q, a]))
    genanki.Package(deck).write_to_file(outfile)
    print(f'🃏  Saved {len(deck.notes)} cards → {outfile}')


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    bullets = summarize(extract_text(pdf_path))
    print(bullets)
    build_deck(bullets)