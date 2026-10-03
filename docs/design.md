# Design

UI, interaction and prompt design. Technical structure is in [architecture.md](architecture.md).

---

## 1. Design principles

1. **Simple first.** Upload, wait, ask. No settings to configure.
2. **Honest answers.** A refusal is a valid answer and should be clear, not hidden.
3. **Show progress.** Anything over a moment gets a spinner.
4. **Stay on the document.** The UI repeats which file you're talking about.

## 2. Screens and states

Built with Streamlit's default layout (centered column, dark theme in the screenshots). Page title `File RAG Assistant`, icon 📄.

| State | What the user sees |
|---|---|
| Missing API key | Red error: "GROQ_API_KEY is missing. Please add it to your .env file." App stops. |
| Landing | Title, one line of intro ("Upload a document and ask questions about it."), file uploader |
| Processing | Spinner: "Processing document..." |
| Ready | Green success: "`<file>` processed successfully!", divider, subheader "Ask about: `<file>`", chat input |
| Answering | User bubble with the question, assistant bubble with spinner "Searching the document..." |
| Answered | Plain-text answer in the assistant bubble |

Screenshots: `Assets/landing_page.png`, `Assets/file_uploaded.png`, `Assets/qa_page.png`.

## 3. Flow

```
open app ─► key present? ──no──► error, stop
               │yes
               ▼
          upload file ─► spinner ─► success banner
                                        │
                                        ▼
                           type question ─► spinner ─► answer
                                        ▲                │
                                        └────────────────┘
```

## 4. Copy

Current strings in `app.py`:

| Where | Text |
|---|---|
| Title | 📄 File RAG Assistant |
| Intro | Upload a document and ask questions about it. |
| Uploader | Upload your file |
| Processing | Processing document... |
| Success | `<name>` processed successfully! |
| Subheader | Ask about: `<name>` |
| Chat input | Ask a question about your file... |
| Searching | Searching the document... |
| Refusal (from the LLM) | I could not find the answer in the uploaded file. |

Tone: short, plain, no jargon.

## 5. Answer design

- Short, factual, plain text.
- Numeric answers should be exact (the sample run returned `8` and `28.4`).
- If the file doesn't contain the answer, the reply is the fixed refusal sentence and nothing else.
- No outside knowledge, no guessing, no "as an AI".

## 6. Prompt design

Rules the model is given (`rag/prompt.py`):

1. Answer only from the provided context.
2. No outside knowledge.
3. Don't make things up.
4. If missing, say the fixed sentence.

Structure: role line → rules → `Context:` → `Question:` → `Answer:`.

A fixed sentence is deliberate. It's easy to read as a user and easy to detect in code later (for refusal-rate tracking).

## 7. Known UX problems

| Problem | Effect | Fix |
|---|---|---|
| Messages aren't saved | Only the latest Q&A shows; scrolling back is impossible | Store messages in `st.session_state` and render the list each run |
| Different file ignored in same session | User uploads file B, still talking to file A | Re-ingest when `uploaded_file.name` changes |
| No sources shown | User can't verify answers | Add "Sources: page 2, page 7" under each answer |
| No streaming | Waits for the full answer | Use `st.write_stream` with `chain.stream` |
| Raw errors on bad files | Stack trace in the UI | `try/except` with `st.error` and a plain message |
| Success banner vanishes on the next interaction | User loses confirmation of which file is loaded | Show a persistent status line tied to the current file |

## 8. Planned UI changes

1. Chat history list.
2. Source citations (page / sheet).
3. "New document" / reset button that clears session and collection.
4. Streaming answers.
5. Basic file info after upload (pages, chunks).
6. Optional sidebar for advanced settings (k, chunk size). Keep hidden by default.

## 9. Accessibility and responsiveness

Streamlit handles layout and basic keyboard use. Nothing custom yet. If a custom theme is added later, keep contrast high and don't rely on color alone for states (use text with the icon).
