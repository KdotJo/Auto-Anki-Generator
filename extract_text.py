import pypdf, sys, textwrap, os
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

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    print(summarize(extract_text(pdf_path)))