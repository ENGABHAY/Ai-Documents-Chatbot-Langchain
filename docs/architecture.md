# Architecture

How the app is put together and why. For requirements see [prd.md](prd.md); for rules of the road see [rules.md](rules.md).

---

## 1. Overview

A two-phase RAG pipeline wrapped in a Streamlit app. Everything runs in one Python process. The only network calls are to the Groq API (generation) and to Hugging Face on first run (embedding model download).

```
Phase 1 - Ingestion (once per uploaded file)

  upload ─► temp file ─► load (by extension) ─► split (1000/150) ─► embed (MiniLM) ─► ChromaDB
                                                                          ▲
                                                                  local, no API cost

Phase 2 - Question answering (once per question)

  question ─► retriever (MMR, k=5, fetch_k=20) ─► format chunks ─► prompt ─► Groq LLM ─► text
                       │
                       └── reads from ChromaDB (./chroma_db)
```

Diagram deck: `workflow_docs/RAG_Workflow.pptx`.

## 2. Runtime view

```
┌──────────────────────── Streamlit process ─────────────────────────┐
│                                                                     │
│  app.py  ── UI + orchestration + session_state                      │
│    │                                                                │
│    ├── loaders/file_loader.py ── routes by extension                │
│    │       └── loaders/excel_loader.py ── 1 Document per sheet      │
│    │                                                                │
│    └── rag/                                                         │
│          splitter.py ─► embeddings.py ─► vectorstore.py             │
│                                              │                      │
│          prompt.py ─► chain.py ◄─────────────┘ (retriever)          │
│                         │                                           │
└─────────────────────────┼───────────────────────────────────────────┘
                          ▼
                 Groq API (openai/gpt-oss-20b)

 Disk: ./chroma_db (vectors + sqlite)     Env: .env → GROQ_API_KEY
```

## 3. Modules

| File | Function | What it does |
|---|---|---|
| `app.py` | (script) | Page config, API key check, file upload, ingestion, chat input and answer. Holds `retriever`, `rag_chain`, `file_name` in `st.session_state`. |
| `loaders/file_loader.py` | `load_file(file_path)` | Picks a loader from the file suffix. Raises `ValueError` for unsupported types. |
| `loaders/excel_loader.py` | `load_excel(file_path)` | Reads every sheet with pandas, turns each into one `Document` via `df.to_string(index=False)`, metadata `{source, sheet}`. |
| `rag/splitter.py` | `split_documents(documents)` | `RecursiveCharacterTextSplitter`, `chunk_size=1000`, `chunk_overlap=150`. |
| `rag/embeddings.py` | `get_embeddings()` | `HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2")`. |
| `rag/vectorstore.py` | `create_vectorstore(docs)`, `create_retriever(vs)` | Chroma persisted to `./chroma_db`; retriever uses MMR with `k=5`, `fetch_k=20`. |
| `rag/prompt.py` | `prompt` | `ChatPromptTemplate` with context-only rules and the fixed refusal sentence. |
| `rag/chain.py` | `create_rag_chain(retriever)`, `format_docs(docs)` | `{context, question} → prompt → ChatGroq → StrOutputParser`. Temperature 0. |

## 4. Loader map

| Extension | Loader |
|---|---|
| `.pdf` | `PyPDFLoader` (one Document per page) |
| `.txt` | `TextLoader` (utf-8) |
| `.docx` | `Docx2txtLoader` |
| `.csv` | `CSVLoader` |
| `.xlsx`, `.xls` | custom `load_excel` |
| `.pptx` | `UnstructuredPowerPointLoader` |
| `.html`, `.htm` | `UnstructuredHTMLLoader` |

## 5. Data model

LangChain `Document`:

```
Document
├── page_content: str
└── metadata: dict   # PDF: source, page · Excel: source, sheet · others: source
```

Metadata survives chunking and is stored in Chroma, so it is available at retrieval time. It is just not shown to the user yet (this is what citations will use).

**Sample run:** 11 pages → 40 chunks, 894 characters on average.

## 6. Configuration

All of this is hardcoded today.

| Setting | Value | Location |
|---|---|---|
| Chunk size / overlap | 1000 / 150 | `rag/splitter.py` |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` | `rag/embeddings.py` |
| Vector store path | `./chroma_db` (default collection) | `rag/vectorstore.py` |
| Retrieval | MMR, `k=5`, `fetch_k=20` | `rag/vectorstore.py` |
| LLM | `openai/gpt-oss-20b` on Groq, `temperature=0` | `rag/chain.py` |
| Secret | `GROQ_API_KEY` from `.env` | `app.py`, `rag/chain.py` |

## 7. State and persistence

- **Session state (per browser session):** `retriever`, `rag_chain`, `file_name`.
- **Disk:** `chroma_db/` persists across runs. Nothing deletes or namespaces it.
- **Temp files:** uploads are written to a temp file with `delete=False` and never removed.
- **Chat history:** not stored. Each question is answered independently.

## 8. Key decisions

| Decision | Why | Trade-off |
|---|---|---|
| LangChain chain (`retriever → prompt → LLM → parser`) | Each stage swappable | Extra dependency; `langchain-community` is being sunset |
| Local MiniLM embeddings | ~90 MB, no API cost | Lower quality than large hosted embeddings |
| ChromaDB on disk | No server to run | Single-machine only |
| MMR retrieval | Avoids five near-duplicate chunks | Weak chunks slip in (2 of 5 on the sample query) |
| Context-only prompt with fixed refusal sentence | Cuts hallucination, easy to detect "not found" | Can falsely refuse when retrieval misses |
| Groq `gpt-oss-20b`, temp 0 | Fast, free tier, consistent answers | External dependency, rate limits |
| Streamlit | Fastest route to a chat UI | Reruns the whole script on every interaction |

## 9. Known gaps

These come straight from reading the code and the notebook's own limitations table.

1. **Collection never reset in `app.py`.** `Chroma.from_documents` appends to `./chroma_db`, and the retriever searches the whole collection. Chunks from earlier uploads can show up in new answers. The notebook resets the collection; the app doesn't.
2. **Second upload ignored in the same session.** Ingestion is guarded by `if "retriever" not in st.session_state`, so a different file is never processed until the session resets.
3. **No chat history on screen.** Messages aren't stored in `session_state`, so each new question replaces the previous exchange.
4. **Temp files leak.** `NamedTemporaryFile(delete=False)` with no cleanup.
5. **No error handling around loading.** Empty text (scanned PDF), corrupt files, or Groq errors surface as raw exceptions.
6. **No citations.** Page and sheet metadata is retrieved but dropped in `format_docs`.
7. **Embedding model is rebuilt** on every `create_vectorstore` call.
8. **`.htm`** is handled in the loader but not allowed in the uploader.

## 10. Security and privacy

- `.env` holds the key and is gitignored. Never commit it or share a zip of the project folder that includes it.
- Retrieved chunks (not the whole file) are sent to Groq with each question.
- `chroma_db/` stores document text on local disk. Treat it as sensitive if documents are.

## 11. Extension points

| Want to change | Touch |
|---|---|
| Add a file type | `loaders/file_loader.py` + `type=[...]` in `app.py` |
| Swap the LLM | `rag/chain.py` (any LangChain chat model) |
| Swap embeddings | `rag/embeddings.py` (re-index required) |
| Swap vector store | `rag/vectorstore.py` |
| Change grounding behavior | `rag/prompt.py` |
| Add citations | `rag/chain.py` (`format_docs` + return metadata) and `app.py` |
