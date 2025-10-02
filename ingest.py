"""
Módulo de ingestión de documentos PDF.

Este script recorre la carpeta 'docs/', extrae texto de los archivos PDF,
genera embeddings con SentenceTransformers y construye un índice semántico
utilizando FAISS. El resultado se guarda en 'store.pkl' para ser usado en app.py.
"""

import os
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

# Inicializar modelo de embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Listas para almacenar documentos y sus rutas
documents = []
paths = []

def extract_text_from_pdf(pdf_path):
    """
    Extrae todo el texto de un archivo PDF.

    Args:
        pdf_path (str): Ruta al archivo PDF.

    Returns:
        str: Texto extraído del PDF.
    """
    reader = PdfReader(pdf_path)
    text_aux = ""
    for page in reader.pages:
        text_aux += page.extract_text() or ""
    return text_aux

# Recorrer recursivamente la carpeta 'docs/' y procesar archivos PDF
for root, _, files in os.walk("docs"):
    for file in files:
        if file.endswith(".pdf"):
            path = os.path.join(root, file)
            text = extract_text_from_pdf(path)
            if text.strip():
                documents.append(text)
                paths.append(path)

# Generar embeddings para los documentos
embeddings = embedder.encode(documents)

# Construir índice FAISS con distancia L2
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Guardar documentos, rutas e índice para uso posterior en app.py
with open("store.pkl", "wb") as f:
    pickle.dump((documents, paths, index), f)

print(f"Ingestados {len(documents)} documentos en el índice.")
