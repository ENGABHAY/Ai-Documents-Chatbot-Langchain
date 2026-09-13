# 📄 AI Documents Chatbot (LangChain + RAG)

A **Retrieval-Augmented Generation (RAG)** chatbot that lets you upload a document and ask questions about it. It extracts, chunks, embeds, and retrieves relevant content from your file, then uses an LLM (via Groq) to generate answers grounded strictly in that document — no hallucinated outside knowledge.

Built with **LangChain**, **ChromaDB**, **HuggingFace embeddings**, **Groq LLM**, and **Streamlit**.

---

## ✨ Features

- 📁 **Multi-format document support** — PDF, TXT, DOCX, CSV, XLSX/XLS, PPTX, HTML
- ✂️ **Smart chunking** using `RecursiveCharacterTextSplitter`
- 🧠 **Local embeddings** via `sentence-transformers/all-MiniLM-L6-v2` (no embedding API cost)
- 🗂️ **Vector search** powered by ChromaDB with MMR (Maximal Marginal Relevance) retrieval
- ⚡ **Fast LLM inference** using Groq (`openai/gpt-oss-20b`)
- 🔒 **Grounded answers only** — the assistant explicitly refuses to answer from outside the uploaded document
- 🖥️ **Simple chat UI** built with Streamlit

---

## 🏗️ How It Works

1. **Upload** a document through the Streamlit UI.
2. **Load** — the file is routed to the correct loader based on its extension (`loaders/file_loader.py`).
3. **Split** — the extracted text is broken into overlapping chunks (`rag/splitter.py`).
4. **Embed & Store** — chunks are embedded and stored in a persistent Chroma vector store (`rag/vectorstore.py`, `rag/embeddings.py`).
5. **Retrieve** — relevant chunks are fetched using MMR search for diverse, relevant context.
6. **Generate** — the retrieved context and your question are passed into a strict, context-only prompt (`rag/prompt.py`) and sent to the Groq LLM (`rag/chain.py`).
7. **Answer** — the response is streamed back to you in the chat interface.

> A visual breakdown of both phases (document ingestion into the vector DB, and question answering) is available in [`workflow_doc/RAG_Workflow.pptx`](workflow_doc/RAG_Workflow.pptx).

---

## 📸 Screenshots

### Landing Page
Upload any supported document to get started.

![Landing Page](Assets/landing_page.png)

### File Processed
Once uploaded, the file is loaded, chunked, embedded, and ready for questions.

![File Uploaded](Assets/file_uploaded.png)

### Question & Answer
Ask natural-language questions and get answers grounded in the document's content.

![Q&A Page](Assets/qa_page.png)

---

## 📂 Project Structure

```
Ai-Documents-Chatbot-Langchain/
├── app.py                     # Streamlit entry point (UI + orchestration)
├── loaders/
│   ├── file_loader.py         # Routes files to the correct loader by extension
│   ├── excel_loader.py        # Custom loader for .xlsx/.xls files
│   └── __init__.py
├── rag/
│   ├── splitter.py            # Document chunking logic
│   ├── embeddings.py          # HuggingFace embedding model config
│   ├── vectorstore.py         # Chroma vector store + retriever setup
│   ├── prompt.py              # Context-only QA prompt template
│   ├── chain.py                # RAG chain (retriever -> prompt -> LLM -> parser)
│   └── __init__.py
├── testfiles/
│   ├── test_loader.py         # Tests for document loaders
│   ├── test_rag.py            # Tests for the RAG pipeline
│   └── test_llm.py            # Tests for LLM connectivity
├── data/uploads/               # Sample files for testing
├── Assets/                     # Screenshots used in this README
├── workflow_doc/
│   └── RAG_Workflow.pptx       # Diagram: ingestion (Phase 1) and Q&A (Phase 2) flow
├── chroma_db/                  # Persisted vector store (auto-generated, gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Component            | Technology                                        |
|-----------------------|----------------------------------------------------|
| Orchestration         | LangChain                                          |
| LLM                    | Groq (`openai/gpt-oss-20b`) via `langchain-groq`   |
| Embeddings             | HuggingFace `all-MiniLM-L6-v2`                     |
| Vector Store           | ChromaDB                                           |
| Document Parsing       | PyPDF, python-docx, openpyxl, pandas, unstructured |
| UI                     | Streamlit                                          |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ENGABHAY/Ai-Documents-Chatbot-Langchain.git
cd Ai-Documents-Chatbot-Langchain
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com).

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📄 Supported File Types

| Format | Loader Used                     |
|--------|----------------------------------|
| PDF    | `PyPDFLoader`                     |
| TXT    | `TextLoader`                      |
| DOCX   | `Docx2txtLoader`                  |
| CSV    | `CSVLoader`                       |
| XLSX/XLS | Custom `excel_loader.py`       |
| PPTX   | `UnstructuredPowerPointLoader`   |
| HTML   | `UnstructuredHTMLLoader`         |

*File size limit: 200MB per file.*

---

## 🧪 Testing

Test scripts are available in `testfiles/`:

```bash
python testfiles/test_loader.py
python testfiles/test_rag.py
python testfiles/test_llm.py
```

---

## 🔮 Future Improvements

- Multi-file / multi-document chat support
- Chat history persistence across sessions
- Source citation with page/section references in answers
- Swappable LLM and embedding providers

---

## 📬 Contact

**Abhay Kadam**
- GitHub: [@ENGABHAY](https://github.com/ENGABHAY)
- LinkedIn: [kadamabhay](https://linkedin.com/in/kadamabhay)
- Email: kadamabhay54@gmail.com
