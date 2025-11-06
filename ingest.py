"""
PDF document ingestion module.

This script recursively scans the 'docs/' folder, extracts text from PDF files, splits the text
into smaller chunks, generates embeddings using SentenceTransformers for each chunk, 
and builds a semantic index with FAISS. 

The resulting index and metadata are saved to 'store.pkl' for use
in the Streamlit application (app.py).
"""

import os
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# Configuration
DOCS_PATH = "docs"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDER_NAME = "all-MiniLM-L6-v2"
STORE_FILE = "store.pkl"

# Initialization
embedder = SentenceTransformer(EMBEDDER_NAME)
documents = []
paths = []

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a given PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text content from the PDF.
    """
    reader = PdfReader(pdf_path)
    text_aux = ""
    for page in reader.pages:
        text_aux += page.extract_text() or ""
    return text_aux

# Chunking
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Splits text into overlapping chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Recursively walk through the directory and process PDF files
for root, _, files in os.walk(DOCS_PATH):
    for file in files:
        if file.endswith(".pdf"):
            path = os.path.join(root, file)
            try:
                text = extract_text_from_pdf(path)
                if text.strip():
                    for chunk in chunk_text(text):
                        documents.append(chunk)
                        paths.append(path)
            except FileNotFoundError:
                print(f"⚠️ File not found, skipping: {path}")
            except Exception as e:
                print(f"⚠️ Error reading {path}: {e}")

# Generate embeddings for all extracted documents
print(f"🧠 Generating embeddings for {len(documents)} text chunks...")
embeddings = embedder.encode(documents, show_progress_bar=True)

# Build FAISS index using L2 distance
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save documents, paths, and index for later use in app.py
with open(STORE_FILE, "wb") as f:
    pickle.dump((documents, paths, index), f)

print(f"Ingested {len(documents)} text chunks from PDFs into {STORE_FILE}.")
