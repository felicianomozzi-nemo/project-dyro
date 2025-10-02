"""
Módulo principal de la demo de asistente de documentación.

Este script utiliza Streamlit para crear una interfaz de consulta en lenguaje natural
sobre documentos previamente indexados en FAISS. Se conecta con un modelo de lenguaje
ejecutado en Ollama para generar respuestas contextuales basadas en la documentación.
"""

import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer
import ollama

# Cargar índice y documentos previamente guardados con ingest.py
with open("store.pkl", "rb") as f:
    documents, paths, index = pickle.load(f)

# Inicializar modelo de embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Título de la aplicación en Streamlit
st.title("🤖 Dyro")

# Entrada de texto para la consulta del usuario
query = st.text_input("Escribí tu consulta sobre la documentación:")

if query:
    # Generar embedding de la consulta
    query_vec = embedder.encode([query])
    _, I = index.search(query_vec, k=2)  # Recuperar los 2 documentos más relevantes

    # Construir contexto a partir de los documentos encontrados
    CONTEXT = "\n".join([documents[i] for i in I[0]])
    refs = [paths[i] for i in I[0]]

    # Preparar prompt para el modelo de lenguaje
    PROMPT = f"Responde en base a la documentación:\n\n{CONTEXT}\n\nPregunta: {query}"

    # Obtener respuesta del modelo Ollama
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": PROMPT}])

    # Mostrar respuesta en pantalla
    st.markdown("### 📖 Respuesta:")
    st.write(response["message"]["content"])

    # Mostrar los documentos consultados
    st.markdown("### 📂 Documentos consultados:")
    for r in refs:
        st.write(f"- {r}")
