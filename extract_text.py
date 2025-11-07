import pypdf, sys, textwrap, os, genanki, re
from tkinter import Tk, filedialog, simpledialog, messagebox
from openai import OpenAI
from pathlib import Path

API_KEY_FILE = Path(os.path.expanduser('~')) / 'openai_api_key.txt'

root = Tk()
root.withdraw()  # hide the main window

if API_KEY_FILE.exists():
    api_key = API_KEY_FILE.read_text(encoding='utf-8').strip()
else:
    api_key = simpledialog.askstring('OpenAI API Key', 'Please enter your OpenAI API key:')
    if not api_key:
        messagebox.showerror('No API Key', 'An OpenAI API key is required to run this application.')
        sys.exit(1)
    API_KEY_FILE.write_text(api_key, encoding='utf-8')
messagebox.showinfo('DEBUG', 'API Key accepted, continuing...')

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    messagebox.showerror('API Error', f'Failed to initialize OpenAI client: {e}')
    sys.exit(1)

pdf_path = filedialog.askopenfilename(
    title='Select PDF File',
    filetypes=[('PDF Files', '*.pdf')]
)

if not pdf_path:
    messagebox.showerror('No File Selected', 'A PDF file must be selected to proceed.')
    sys.exit(1)

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

if hasattr(sys, '_MEIPASS'):
    prompt_path = os.path.join(sys._MEIPASS, 'prompt.txt')
else:
    prompt_path = 'prompt.txt'

try:
    prompt = Path(prompt_path).read_text(encoding='utf-8')
except Exception as e:
    messagebox.showerror('Prompt Error', f'Failed to read prompt file: {e}')
    sys.exit(1)

def summarize(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user",   "content": f"Lecture notes:\n{text[:5000]}"}
            ],
            temperature=0.25
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        messagebox.showerror('OpenAI Error', f'Failed to get response from OpenAI: {e}')
        sys.exit(1) 

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
    cards = []
    current_q = None
    answer_lines = []

    for line in bullets.splitlines():
        line = line.rstrip()
        if not line:
            continue

        if line.startswith('• '):
            if current_q is not None:
                cards.append((current_q, '\n'.join(answer_lines)))
            current_q = line[2:].strip()
            answer_lines = []
            continue
        if line.startswith('  - ') and current_q is not None:
            answer_lines.append(line[4:].strip() + '<br>' + '<br>')
            continue
    if current_q is not None:
        cards.append((current_q, '\n'.join(answer_lines)))
    return cards

def build_deck(bullets: str):
    save_path = filedialog.asksaveasfilename(
        title='Save Anki Deck As',
        defaultextension='.apkg',
        filetypes=[('Anki Deck Package', '*.apkg')],
        initialfile='lecture_deck.apkg'
    )
    if not save_path:
        messagebox.showerror('No Save Location', 'You must specify a location to save the Anki deck.')
        sys.exit(1)
    deck = genanki.Deck(DECK_ID, 'Lecture Deck')
    for q, a in _qa(bullets):
        deck.add_note(genanki.Note(model=MODEL, fields=[q, a]))
    genanki.Package(deck).write_to_file(save_path)
    messagebox.showinfo('Success', f'🃏  Saved {len(deck.notes)} cards → {save_path}')

if __name__ == "__main__":
    try:
        text = extract_text(pdf_path)
        bullets = summarize(text)
        build_deck(bullets)
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')
        sys.exit(1)