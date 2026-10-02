# Project Memory

Running context for anyone (or any AI assistant) picking this project up. Read this first. Keep it current.

**Last updated:** 2026-10-02

---

## What this is

RAG chatbot for one uploaded document. Streamlit UI, LangChain pipeline, local MiniLM embeddings, ChromaDB, Groq LLM. Built by Abhay Kadam as a portfolio project and as a submission notebook.

Repo: `github.com/ENGABHAY/Ai-Documents-Chatbot-Langchain`

## Current state

- Pipeline works end to end in both the app and the notebook.
- Notebook (`AI_Documents_Chatbot_LangChain.ipynb`) is saved with outputs and lives on the `notebook-submission` branch.
- Known bugs in `app.py` are listed in `tasks.md` under P0. The notebook already resets the Chroma collection; the app does not.
- Evidence of quality is a 4-question smoke test only.

## Key facts

| Item | Value |
|---|---|
| Python | 3.13 (from compiled `.pyc` files) |
| Dev OS | Windows (old test paths are `D:\VS code\Rag using langchain\...`) |
| LLM | Groq `openai/gpt-oss-20b`, temperature 0 |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2`, local, ~90 MB |
| Chunking | `RecursiveCharacterTextSplitter` 1000 / 150 |
| Retrieval | MMR, `k=5`, `fetch_k=20` |
| Vector store | Chroma at `./chroma_db`, default collection |
| Sample doc | `data/uploads/NIPS-2017-attention-is-all-you-need-Paper.pdf` (11 pages → 40 chunks, avg 894 chars) |
| Secret | `GROQ_API_KEY` in `.env` |
| Run | `streamlit run app.py` → http://localhost:8501 |

## Decisions log

| Decision | Reason |
|---|---|
| Context-only prompt with one fixed refusal sentence | Reduce hallucination, make "not found" detectable |
| Local embeddings | No embedding API cost |
| MMR over plain similarity | Avoid near-duplicate chunks |
| One Excel sheet = one Document | Keeps sheet name in metadata |
| Temperature 0 | Consistent, factual answers |
| Notebook resets the collection each run | So re-running with another file doesn't mix old chunks |
| All planning docs go in `docs/`; only `README.md` stays at root | Keeps root clean |

## Gotchas

1. **App appends to Chroma, never clears it.** Delete `chroma_db/` by hand between tests until the fix lands.
2. **Second upload in one session does nothing.** Refresh the page to switch files.
3. **Only the latest Q&A is visible.** Not stored in session state.
4. **Strict prompt can false-refuse** if retrieval misses the right chunk. Check refusals against the source.
5. **Scanned PDFs return little or no text.** No OCR.
6. **PDF artifacts:** ligatures (`ﬁ`), odd spacing (`[ 11]`), flattened math, no tables.
7. **Warnings that are safe to ignore:** `langchain-community` sunset notice, `tqdm`/`ipywidgets` notice, Hugging Face unauthenticated-request notice (set `HF_TOKEN` to silence).
8. **`.gitignore` pycache line is malformed** (`**pycache**/`).
9. **Do not share project zips with `.env` inside.**
10. Test scripts have hardcoded Windows paths and will fail elsewhere.

## Reference results (sample paper)

| Question | Answer | Result |
|---|---|---|
| What is self-attention? | Relates different positions of a single sequence to compute a representation of it | Correct |
| Attention heads in the base Transformer? | 8 | Correct |
| BLEU of the big model, EN→DE? | 28.4 | Correct |
| Who won the 2018 FIFA World Cup? | I could not find the answer in the uploaded file. | Correct refusal |

This is a smoke test, not a benchmark. Retrieval for "What is self-attention?" returned 2 weak chunks out of 5 (positional-encoding formula, reference list).

## Branches

| Branch | Purpose |
|---|---|
| `main` | Stable app, README, workflow doc |
| `app_files` | Earlier app file work |
| `notebook-submission` | Adds the end-to-end notebook with outputs |

## Conventions to remember

- Plain, human-sounding writing. No inflated language.
- Don't invent numbers. State what was and wasn't measured.
- Minimal changes to existing files unless asked.
- Runnable code blocks, delivered step by step with the output explained before moving on.
- Details live in `rules.md`.

## Doc map

| File | Purpose |
|---|---|
| `prd.md` | What and why |
| `architecture.md` | How it's built |
| `design.md` | UI and prompt design |
| `rules.md` | Conventions and guardrails |
| `tasks.md` | Bugs and backlog |
| `memory.md` | This file |

## Changelog

- 2026-10-02: Added `docs/` (prd, architecture, design, rules, tasks, memory). Updated README project structure.
