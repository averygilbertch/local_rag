import os
import PyPDF2

DOCS_DIR = "./docs/"
OUTPUT_FILE = "./vault.txt"
CHUNK_SIZE = 1000

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file using PyPDF2."""
    text = []
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return "\n".join(text)

def chunk_text(text, chunk_size):
    """Splits text into chunks of a given size while preserving line breaks."""
    words = text.split()  # Split text into words to avoid cutting in the middle of words
    chunks = []
    chunk = []

    for word in words:
        if sum(len(w) for w in chunk) + len(chunk) + len(word) > chunk_size:
            chunks.append(" ".join(chunk))  # Join words to form a chunk
            chunk = []
        chunk.append(word)

    if chunk:
        chunks.append(" ".join(chunk))  # Add last chunk

    return chunks

def process_pdfs():
    """Processes all PDFs in the docs directory and appends text chunks to the output file."""
    with open(OUTPUT_FILE, "a", encoding="utf-8") as out_file:
        for filename in os.listdir(DOCS_DIR):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(DOCS_DIR, filename)
                print(f"Processing: {pdf_path}")
                
                text = extract_text_from_pdf(pdf_path)
                if text.strip():
                    chunks = chunk_text(text, CHUNK_SIZE)
                    for chunk in chunks:
                        out_file.write(chunk + "\n\n")  # Each chunk as a separate line with a blank line between

if __name__ == "__main__":
    process_pdfs()
    print(f"Text extraction completed. Data saved to {OUTPUT_FILE}")
