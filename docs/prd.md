# Product Requirements Document (PRD)

**Project:** AI Documents Chatbot (LangChain + RAG)
**Owner:** Abhay Kadam
**Status:** Prototype working (notebook + Streamlit app). Hardening in progress.
**Last updated:** 2026-10-02

---

## 1. Summary

A chatbot that answers questions from one uploaded document. It finds the relevant passages, hands only those to an LLM, and tells the LLM to answer from them or say it couldn't find the answer. The point is answers you can check, not answers that sound good.

## 2. Problem

People who work with long documents (papers, reports, notes, spreadsheets) lose time hunting for one specific fact.

- Keyword search misses paraphrased wording.
- Asking a general LLM directly is risky: it hasn't seen the document and may answer from memory or invent something.

## 3. Target users

| User | What they need |
|---|---|
| Students and researchers | Quick, exact facts from papers (model sizes, scores, definitions) |
| Professionals | Answers from private reports or spreadsheets without reading end to end |
| Reviewers of this project (recruiters, interviewers) | A clear, runnable RAG example with honest limitations |

## 4. Goals

1. Upload one file and ask questions in plain English.
2. Answers come only from that file, or an explicit "not found".
3. Works with common office formats, not just PDF.
4. Runs cheaply: local embeddings, free-tier hosted LLM.
5. Easy to set up: clone, add one API key, run.

## 5. Non-goals (for now)

- Multi-document or whole-folder chat
- User accounts, auth, or multi-tenant storage
- OCR for scanned documents
- Chat memory across sessions
- Production-grade hosting or scaling

## 6. User stories

- As a user, I upload a PDF so I can ask questions about it.
- As a user, I get "I could not find the answer in the uploaded file." instead of a guess when the file doesn't cover my question.
- As a user, I upload a spreadsheet and ask about a value in a sheet.
- As a user, I want to see where an answer came from so I can verify it. *(not built yet)*
- As a user, I ask a follow-up like "what about the big model?" and it understands. *(not built yet)*

## 7. Functional requirements

| ID | Requirement | Status |
|---|---|---|
| FR-1 | Accept uploads: PDF, TXT, DOCX, CSV, XLSX/XLS, PPTX, HTML | Done |
| FR-2 | Route each file to the correct loader by extension | Done |
| FR-3 | Split text into overlapping chunks (1000 / 150) | Done |
| FR-4 | Embed chunks locally and store in ChromaDB | Done |
| FR-5 | Retrieve with MMR (k=5, fetch_k=20) | Done |
| FR-6 | Answer through a context-only prompt with a fixed refusal sentence | Done |
| FR-7 | Chat UI with spinner while processing and searching | Done |
| FR-8 | Block the app with a clear message if `GROQ_API_KEY` is missing | Done |
| FR-9 | Process a new file when the user uploads a different one | **Open bug** |
| FR-10 | Isolate each upload's chunks so old files never leak into answers | **Open bug** |
| FR-11 | Show full conversation history on screen | **Open bug** |
| FR-12 | Cite page / sheet for each answer | Planned |
| FR-13 | Follow-up questions with chat history and query rewriting | Planned |
| FR-14 | Multi-file chat | Planned |

## 8. Non-functional requirements

| Area | Requirement |
|---|---|
| Cost | No paid embedding API. LLM on Groq free tier. |
| Privacy | Document text goes to Groq only as retrieved chunks. Embedding and storage stay local. API key never committed. |
| Reliability | Unsupported or unreadable files should fail with a readable message, not a stack trace. *(partly missing)* |
| Performance | Ingestion of a ~11-page PDF in seconds; answers in a few seconds. *(not formally measured)* |
| Portability | Python 3.13 tested. Windows dev, should run on macOS/Linux. |
| Size | Streamlit default upload cap of 200 MB per file. |

## 9. Success metrics

Right now the only evidence is a smoke test on one paper (*Attention Is All You Need*): 3 of 3 in-document questions correct, 1 of 1 out-of-scope question correctly refused. That shows the pipeline works. It is not an accuracy number.

Targets once an evaluation set exists:

| Metric | Target |
|---|---|
| Answer correctness on a 30-50 question set | Track, then set a bar after the first run |
| Faithfulness (answer supported by retrieved text) | Track with RAGAS or similar |
| False refusal rate (in-document question refused) | Track, aim to drive down |
| Out-of-scope refusal rate | Should stay near 100% |

## 10. Constraints and assumptions

- One document at a time.
- Text-based files only. Scanned PDFs will return little or nothing.
- Depends on Groq being reachable and the `openai/gpt-oss-20b` model being available.
- `langchain-community` is being sunset, so loaders will need migrating eventually.

## 11. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Retrieval returns weak chunks | Diluted or wrong answers on big files | Relevance threshold, reranker, tune k |
| Strict prompt refuses when retrieval misses | False "not found" | Track refusal rate, spot-check refusals |
| Old uploads stay in ChromaDB | Answers mix documents | Reset or namespace collection per upload (FR-10) |
| PDF extraction artifacts (ligatures, flattened math, tables) | Poor chunks | Clean text, layout-aware parser for table-heavy files |
| Model name or provider change | App stops working | Make LLM and embeddings swappable |

## 12. Roadmap

**Now (fix what's broken)**
FR-9, FR-10, FR-11, temp file cleanup, readable error messages.

**Next (make answers checkable)**
Source citations (FR-12), evaluation set, relevance threshold.

**Later**
Chat history and query rewriting (FR-13), multi-file chat (FR-14), swappable providers, deployment.

## 13. Open questions

- Which hosting target, if any (Streamlit Community Cloud, Hugging Face Spaces)?
- Keep one shared collection with per-file metadata filters, or one collection per upload?
- Is OCR in scope for scanned documents?
