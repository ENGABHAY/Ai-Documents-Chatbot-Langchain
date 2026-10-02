# Tasks

Single source of truth for what's done, what's broken and what's next. Update it when you finish something.

Legend: `[x]` done · `[ ]` open · **P0** fix first · **P1** next · **P2** later

---

## Done

- [x] Streamlit app: upload → process → chat (`app.py`)
- [x] Loaders for PDF, TXT, DOCX, CSV, XLSX/XLS, PPTX, HTML
- [x] Custom Excel loader (one Document per sheet)
- [x] Splitter, embeddings, Chroma vector store, MMR retriever
- [x] Context-only prompt with fixed refusal sentence
- [x] RAG chain on Groq `openai/gpt-oss-20b`, temperature 0
- [x] Test scripts in `testfiles/` (loader, RAG, LLM)
- [x] RAG workflow diagram deck (`workflow_docs/RAG_Workflow.pptx`)
- [x] README with design choices, setup, sample results
- [x] End-to-end notebook with saved outputs, observations, limitations (branch `notebook-submission`)
- [x] Smoke test on the sample paper: 3/3 correct, 1/1 correct refusal

---

## P0 - Bugs

- [ ] **Reset or namespace the Chroma collection per upload.**
  `Chroma.from_documents` appends to `./chroma_db`, so old files bleed into new answers.
  *Done when:* upload file A, then file B, and a question only B can answer works, and a question only A can answer is refused.
- [ ] **Handle a second upload in the same session.**
  `if "retriever" not in st.session_state` blocks re-ingestion.
  *Done when:* switching files rebuilds retriever and chain, and the subheader shows the new name.
- [ ] **Keep chat history on screen.**
  Store `messages` in `st.session_state`, render them each run.
  *Done when:* three questions in a row all stay visible.
- [ ] **Delete the temp file after loading.**
  Wrap in `try/finally` and `os.remove`.

---

## P1 - Reliability and quality

- [ ] Friendly errors: unsupported type, empty text (scanned PDF), Groq failure. Use `st.error`, no stack traces.
- [ ] Add `.htm` to the uploader list (loader already supports it).
- [ ] Fix `.gitignore`: `**pycache**/` → `__pycache__/`.
- [ ] Make tests portable: remove `D:\...` paths, add `sys.path` setup to `test_rag.py`, remove the duplicate import in `test_loader.py`, add real assertions.
- [ ] Cache the embedding model (`st.cache_resource`) so it isn't rebuilt per upload.
- [ ] Add `.env.example` with `GROQ_API_KEY=`.
- [ ] Source citations: return page / sheet with each answer.
- [ ] Build an evaluation set of 30-50 questions with reference answers. Score correctness, faithfulness and false-refusal rate (RAGAS or a simple script).
- [ ] Retrieval tuning: relevance score threshold, try other `k`/`fetch_k`, skip reference-list pages.

---

## P2 - Features

- [ ] Chat history in the prompt and query rewriting for follow-ups.
- [ ] Streaming answers.
- [ ] "New document" button that clears session and collection.
- [ ] Show file stats after upload (pages, chunks).
- [ ] Multi-file chat with per-file metadata filtering.
- [ ] Swappable LLM and embedding providers via config.
- [ ] Layout-aware parsing for table-heavy PDFs; text cleanup for ligatures and spacing.
- [ ] Migrate loaders off `langchain-community`.
- [ ] Pin dependency versions.
- [ ] Deploy (Streamlit Community Cloud or Hugging Face Spaces) and add the link to the README.
- [ ] Optional OCR for scanned documents.

---

## Docs

- [x] `docs/prd.md`
- [x] `docs/architecture.md`
- [x] `docs/rules.md`
- [x] `docs/design.md`
- [x] `docs/tasks.md`
- [x] `docs/memory.md`
- [ ] Add `docs/` and its files to the README project structure (replace root README with the updated one)
- [ ] Re-check docs after each P0 fix

---

## Suggested order

1. Collection reset
2. Second-upload handling
3. Chat history
4. Temp file cleanup
5. Friendly errors
6. Evaluation set
7. Citations
