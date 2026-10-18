# Comparing Context Strategies: Local SLM vs Gemini, With and Without a Vector DB

## 1. Setup

| Item | Value |
| --- | --- |
| Curated corpus | `context_sample/`: 14 Markdown files about a synthetic persona, about 23,000 characters (about 5,700 tokens by Gemini's count) |
| Local answer model | `phi4-mini:3.8b-q4_K_M` via Ollama, context window 4,096 tokens (script default) |
| Frontier answer model | `gemini-3.8-flash`, free tier |
| Vector DB | Chroma with local `all-minilm` embeddings; 53 chunks of up to 600 characters; top 3 chunks retrieved per question |
| Questions | 12 fixed questions in `eval/questions.json`: direct facts, preferences, synthesis, contradictions, absent evidence, relationships |
| Machine | MacBook Pro (personal laptop) |

The four configurations:

| | No vector DB (Level 1: all notes in the prompt) | With vector DB (Level 2: top 3 chunks) |
| --- | --- | --- |
| **Phi-4 Mini (local)** | A | B |
| **Gemini Flash (cloud)** | C | D |

Within each level, both models received identical prompts. Full answers are in [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md); raw reports are in [`results/`](results/) and [`logs/`](logs/); screenshots are in [`screenshots/`](screenshots/).

## 2. Results at a glance

| Config | Correct | Partial | Wrong | Failed to run | Median seconds | Median prompt size |
| --- | --- | --- | --- | --- | --- | --- |
| A. Phi-4 Mini, no vector DB | 5 | 3 | 4 | 0 | 77.4 | 23,355 chars |
| B. Phi-4 Mini, vector DB | 7 | 1 | 4 | 0 | 21.2 | 1,953 chars |
| C. Gemini Flash, no vector DB | 11 | 0 | 0 | 1 | 5.0 | 23,355 chars |
| D. Gemini Flash, vector DB | 4 | 3 | 2 | 3 | 3.7 | 1,953 chars |

Per question (Correct / Partial / Wrong / Error):

| Question | A. Phi, no VDB | B. Phi, VDB | C. Gemini, no VDB | D. Gemini, VDB |
| --- | --- | --- | --- | --- |
| q01 deadline and advisor | Correct | Wrong | Correct | Partial |
| q02 moisture threshold | Correct | Correct | Correct | Error (503) |
| q03 "tl;dr" and emoji rules | Wrong | Correct | Correct | Correct |
| q04 best time for hard work | Correct | Correct | Correct | Correct |
| q05 capstone tools, why no deep learning | Partial | Partial | Correct | Partial |
| q06 current editor (contradiction) | Wrong | Wrong | Correct | Wrong |
| q07 firmware language (contradiction) | Partial | Wrong | Correct | Wrong |
| q08 favorite movie (absent) | Wrong | Correct | Correct | Correct |
| q09 desktop GPU (absent) | Correct | Correct | Correct | Correct |
| q10 people on the capstone | Partial (3 of 4) | Wrong | Correct (4 of 4) | Partial (2 of 4) |
| q11 Chroma vs pgvector | Wrong | Correct | Correct | Error (429) |
| q12 key themes | Correct | Correct | Error (429) | Error (429) |

Scores are my own judgment against the expected answers in `eval/questions.json`. The vector DB retrieved at least one chunk from 12 of the 23 files that held the answers (52%).

## 3. What I observed

**Context window limits (A vs C).** My notes were about 5,700 tokens, but Phi-4 Mini only had room for 4,096, so part of every Level 1 prompt was cut off. The failures fit that: Phi-4 Mini said there was no information about Chroma vs pgvector (q11) or about my code editor (q06), even though both were in the notes. On q08 it lost the instructions at the top of the prompt entirely and answered as a generic chatbot ("my knowledge cutoff date in September 2021"). On q03 it explained what "tl;dr" generally means instead of using my stated preference. Gemini received the identical prompt, had room for all of it, and answered 11 of 11 completed questions correctly.

**Effect of the vector DB on the local model (A vs B).** Retrieval shrank the prompt about 12 times (23,355 to 1,953 characters), so Phi-4 Mini could finally see everything it was given. It became 3.6 times faster (77 to 21 seconds) and fixed q03, q08, and q11. But it failed in new ways when retrieval picked the wrong chunks. On q01 the chunk with the deadline was not retrieved, so it said the deadline was "shortly after" the real date and cited a chunk that did not contain it. On q10 it called my code-review partner Sam Chen my "instructor," apparently mixing in a retrieved reading-list chunk.

**Effect of the vector DB on Gemini (C vs D).** With a corpus this small, retrieval made Gemini worse. Gemini could already read everything, so limiting it to 3 chunks only removed information. It found 2 of 4 people on q10 instead of 4 of 4 and missed the contradictions. Retrieval saved little time (5.0 to 3.7 seconds), though it did cut the tokens sent per request.

**Contradictions and recency (q06, q07).** This was the clearest difference. Gemini with all notes was the only configuration to notice that my October journal replaces older notes (VS Code to Zed, Rust to MicroPython, 15 to 30 minutes). With the vector DB, q07 retrieved three chunks from the old garden-sensor file and none from the journal. Both models then stated the outdated answer confidently and said "there is no conflicting information." That is the most dangerous failure in the test, because the answer looked sure of itself and cited a real source.

**Absent evidence (q08, q09).** Almost every configuration correctly said the information was missing. The one exception was Phi-4 Mini without the vector DB on q08, caused by the cut-off prompt described above. Retrieval helped the small model here, because the instruction to answer only from the sources stayed inside the window.

**Relationships (q10).** Only Gemini with all notes found all four people. Every other configuration missed Marcus Lee, whose connection to the project is only described in the people file. Top-3 retrieval cannot collect facts spread across several files.

**Latency and cost.** Phi-4 Mini is free and keeps my notes on my laptop, but it took 77 seconds per answer with all notes. Gemini answered in about 4 to 5 seconds, but the free tier allowed only 20 requests per day. This test needed 24, so three runs failed with a quota error (429) and one failed because the model was overloaded (503). Gemini's free tier may also use submitted content to improve Google's products, which is why my notes are synthetic.

## 4. Conclusions

For a personal context folder this small, sending everything to Gemini (config C) gave by far the best answers, including the only correct handling of outdated information. The vector DB is what made the local model usable, because it fit the prompt inside Phi-4 Mini's small window. But top-3 retrieval missed the right chunk about half the time, and when it did, both models either said the information was missing or confidently repeated outdated facts. If my notes grew 10 or 100 times larger, sending everything would stop being possible even for Gemini, so retrieval would become necessary. At that point I would need better retrieval (more chunks, or a graph for relationship questions) and notes curated so that outdated facts are updated or removed rather than left beside the new ones. The biggest curation lesson is that a dated journal entry is not enough to supersede an older file: when a fact changes, the original file should be updated too.

## 5. Limitations of this comparison

- One run per configuration per question. Model outputs vary between runs.
- Four Gemini runs failed (one 503, three 429 daily-quota errors) and were not rerun.
- The scores are my own judgment.
- Token counts differ between tokenizers, so the overflow amount is approximate.
- The corpus is a small synthetic persona, so results may not generalize to large real document sets.
