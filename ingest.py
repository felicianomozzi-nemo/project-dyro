"""
PDF document ingestion module.

This script recursively scans the 'docs/' folder, extracts text from PDF files,
generates embeddings using SentenceTransformers, and builds a semantic index
with FAISS. The resulting index and metadata are saved to 'store.pkl' for use
in the Streamlit application (app.py).
"""

import os
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# Initialize the embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Lists to store extracted documents and their corresponding file paths
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

# Recursively walk through the 'docs/' directory and process PDF files
for root, _, files in os.walk("docs"):
    for file in files:
        if file.endswith(".pdf"):
            path = os.path.join(root, file)
            try:
                text = extract_text_from_pdf(path)
                if text.strip():
                    documents.append(text)
                    paths.append(path)
            except FileNotFoundError:
                print(f"⚠️ File not found, skipping: {path}")
            except Exception as e:
                print(f"⚠️ Error reading {path}: {e}")

# Generate embeddings for all extracted documents
embeddings = embedder.encode(documents)

# Build FAISS index using L2 distance
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save documents, paths, and index for later use in app.py
with open("store.pkl", "wb") as f:
    pickle.dump((documents, paths, index), f)

print(f"Ingested {len(documents)} documents into the index.")
