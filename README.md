# 🤖 Dyro

This project is a prototype of a **conversational assistant** that allows users to query internal documentation using natural language.
The assistant uses a **RAG (Retrieval-Augmented Generation)** pipeline with embeddings, semantic search, and a language model.

---

## 📂 Project Structure

```
project/
│
├── docs/                # Folder containing PDFs organized by category
│   └── Products/
│       └── Hotels/
│           ├── hotel1.pdf
│           └── hotel2.pdf
│
├── ingest.py            # Script that processes PDFs and builds the index
├── app.py               # Streamlit web interface for interacting with the assistant
├── requirements.txt     # Project dependencies
└── .pylintrc            # Pylint configuration for code quality checks
```

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone <REPO_URL>
   cd project
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama** (to run a local language model)

   * [Download Ollama](https://ollama.ai/)
   * Once installed, make sure you have a model available, for example:

     ```bash
     ollama run llama3
     ```

---

## 🚀 Usage

1. **Prepare your documents**
   Place your PDFs inside the `docs/` folder, following the folder structure you want to reflect.

2. **Ingest the documents and build the index**

   ```bash
   python ingest.py
   ```

   This will create a `store.pkl` file containing the extracted text and the semantic index.

3. **Run the web application**

   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   The interface will be available at [http://localhost:8501](http://localhost:8501).

---

## 🧰 Technologies Used

* [Streamlit](https://streamlit.io/) → fast and simple web interface.
* [Sentence Transformers](https://www.sbert.net/) → embedding generation.
* [FAISS](https://faiss.ai/) → semantic search.
* [Ollama](https://ollama.ai/) → local execution of language models (e.g., Llama 3).
* [PyPDF](https://pypi.org/project/pypdf/) → text extraction from PDF files.

---

## 📝 Notes

* The project is configured with **Pylint** (`.pylintrc`) to maintain a consistent coding style.
* This prototype does not include authentication or access control — do not use it in production without additional security measures.
* The accuracy of responses depends on the quality of the documents and the language model used.