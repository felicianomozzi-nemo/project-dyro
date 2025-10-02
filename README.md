# 🤖 Dyro

Este proyecto es un prototipo de **asistente conversacional** que permite consultar documentación interna en lenguaje natural.
El asistente utiliza un pipeline de **RAG (Retrieval-Augmented Generation)** con embeddings, búsqueda semántica y un modelo de lenguaje.

---

## 📂 Estructura del proyecto

```
project/
│
├── docs/                # Carpeta con PDFs organizados por categorías
│   └── Productos/
│       └── Hoteles/
│           ├── hotel1.pdf
│           └── hotel2.pdf
│
├── ingest.py            # Script que procesa PDFs y construye el índice
├── app.py               # Interfaz web en Streamlit para interactuar con el asistente
├── requirements.txt     # Dependencias del proyecto
└── .pylintrc            # Configuración de Pylint para control de calidad
```

---

## ⚙️ Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <URL_DEL_REPO>
   cd project
   ```

2. **Crear y activar un entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar Ollama** (para usar el modelo de lenguaje local)

   * [Descargar Ollama](https://ollama.ai/)
   * Una vez instalado, asegurarse de tener disponible un modelo, por ejemplo:

     ```
     ollama run llama3
     ```

---

## 🚀 Uso

1. **Preparar los documentos**
   Colocar los PDFs en la carpeta `docs/` siguiendo la estructura de carpetas que quieras reflejar.

2. **Ingestar los documentos y construir el índice**

   ```bash
   python ingest.py
   ```

   Esto genera el archivo `store.pkl` con los textos y el índice semántico.

3. **Ejecutar la aplicación web**

   ```bash
   streamlit run app.py
   ```

4. **Abrir el navegador**
   La interfaz se mostrará en [http://localhost:8501](http://localhost:8501).

---

## 🧰 Tecnologías utilizadas

* [Streamlit](https://streamlit.io/) → interfaz web rápida y simple.
* [Sentence Transformers](https://www.sbert.net/) → generación de embeddings.
* [FAISS](https://faiss.ai/) → búsqueda semántica.
* [Ollama](https://ollama.ai/) → ejecución local de modelos de lenguaje (ej. Llama 3).
* [PyPDF](https://pypi.org/project/pypdf/) → extracción de texto desde PDFs.

---

## 📝 Notas

* El proyecto está configurado con **Pylint** (`.pylintrc`) para mantener un estilo de código consistente.
* Este prototipo no incluye autenticación ni control de acceso: no usar en producción sin medidas adicionales.
* La precisión de las respuestas depende de la calidad de los documentos y del modelo de lenguaje.
