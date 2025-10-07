import pypdf, sys

def extract_text(pdf_path):
    # Opens the PDF file
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)  
        text = ""
        # Extracts the text from each page and adds it to the text variable
        for page in reader.pages:
            text += page.extract_text()
        return text

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    print(extract_text(pdf_path))