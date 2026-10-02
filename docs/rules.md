# Project Rules

The ground rules for working on this repo, whether you're a person or an AI assistant. Short on purpose.

---

## 1. Answering rules (non-negotiable product behavior)

1. The bot answers **only** from retrieved document chunks.
2. If the answer isn't in the context, it replies with exactly:
   `I could not find the answer in the uploaded file.`
3. Never loosen the prompt to make answers "more helpful" at the cost of grounding.
4. Keep `temperature=0`.
5. Don't change the refusal sentence without updating `rag/prompt.py`, the README, the notebook, and anything that string-matches it.

## 2. Secrets and data

- `GROQ_API_KEY` lives in `.env` only. Never hardcode it, print it, or paste it into the notebook.
- `.env` and `chroma_db/` stay out of git. Don't zip the project for sharing without removing `.env` first.
- Don't commit user documents. `data/uploads/` holds only the public sample paper.
- Treat `chroma_db/` as containing document text.

## 3. Code style

- Python 3.13, PEP 8, 4-space indent.
- One responsibility per module. UI logic in `app.py`, file parsing in `loaders/`, pipeline in `rag/`.
- Functions take plain inputs and return plain outputs. No hidden globals.
- No hardcoded absolute paths. Use `pathlib` and paths relative to the repo.
- Add a type hint and one-line docstring to any new function.
- Prefer small, readable functions over clever chains.

## 4. Layout rules

- All planning/spec markdown lives in `docs/`. Only `README.md` stays at the root.
- Notebook code must mirror the app code. If you change a parameter in `rag/`, change it in the notebook too (and the README design table).
- New loaders go in `loaders/` and are registered in `file_loader.py`.

## 5. Dependencies

- Add to `requirements.txt` when you import something new.
- Keep it flat and readable. Pin versions before any deployment.
- Prefer standalone integration packages (`langchain-chroma`, `langchain-groq`, `langchain-huggingface`) over `langchain-community` for new code.

## 6. Changing RAG parameters

Any change to chunk size, overlap, embedding model, `k`, or `fetch_k` must:

1. Be re-run on the sample paper and the four reference questions (see below).
2. Update the README design table and `docs/architecture.md`.
3. Note the reason in `docs/memory.md`.
4. Re-index: changing the embedding model or chunking means deleting the old collection.

**Reference questions (sample paper):**

| Question | Expected |
|---|---|
| What is self-attention? | Relates different positions of a single sequence to compute a representation of it |
| Attention heads in the base Transformer? | 8 |
| BLEU of the big model, English to German? | 28.4 |
| Who won the 2018 FIFA World Cup? | `I could not find the answer in the uploaded file.` |

## 7. Testing

- `testfiles/` scripts must run from the repo root on any machine. No `D:\...` paths.
- A test should assert something, not just print.
- Anything touching Groq is an integration test and needs the key. Keep loader and splitter tests offline.
- Before a PR: run loader test, RAG test, and the four reference questions.

## 8. Git

- Branches: `main` is stable. Use a short-lived branch per change (past examples: `app_files`, `notebook-submission`).
- Commit messages: imperative and specific ("Reset Chroma collection per upload"), not "update" or "delete".
- Don't commit `__pycache__/`, `.ipynb_checkpoints/`, `venv/`.
- The current `.gitignore` has `**pycache**/`, which looks mangled by markdown. The working pattern is `__pycache__/`.

## 9. Docs

- Write plainly. Short sentences, real numbers, no filler.
- Don't invent results. If something wasn't measured, say so. The notebook's "four questions is a smoke test, not a benchmark" is the tone to keep.
- Update `docs/tasks.md` when a task is done and `docs/memory.md` when a decision is made.

## 10. For AI assistants working in this repo

- Read `docs/memory.md` first, then `docs/tasks.md`.
- Make minimal, targeted changes. Don't refactor unrelated files.
- Don't touch `.env` or print its contents.
- Deliver changes step by step and explain what the output means before moving on.
- If a fix changes behavior, say which doc needs updating.
