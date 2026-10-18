# Context Curation: Making My AI Agent Personal

Studio assignment, Steps 1 and 2 of [`instructions.md`](instructions.md): give an AI agent a curated personal context, then compare a local small language model (Phi-4 Mini) with a frontier model (Gemini Flash), with and without a vector database.

| Deliverable | Where |
| --- | --- |
| Curated context folder | [`context_sample/`](context_sample/) |
| Fixed evaluation questions and expected answers | [`eval/questions.json`](eval/questions.json) |
| Raw results (JSON reports and terminal logs) | [`results/`](results/), [`logs/`](logs/) |
| Generated results summary | [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md) |
| Screenshots | [`screenshots/`](screenshots/) |
| Comparison write-up | [`COMPARISON.md`](COMPARISON.md) |
| Stretch: graph DB analysis | [`STRETCH_GRAPHDB.md`](STRETCH_GRAPHDB.md) |

## The curated context

`context_sample/` describes a synthetic persona, Jordan Okafor, a data analyst studying applied AI part-time. It is written the way I would want my own context written for an assistant. It contains no secrets or real personal data, because Gemini's free tier may use submitted content and this repository is public.

```
context_sample/
  profile/        about_me, communication_style, interests_and_life
  preferences/    tools_and_stack
  work/           day_job
  projects/       capstone_member_churn, garden_sensor, portfolio_plan
  schedule/       weekly_routine
  people/         collaborators
  learning/       studio_notes, reading_list
  decisions/      decision_log
  journal/        2026-10_reflections
```

Curation choices:

- **One topic per file, with headings.** This gives Level 2 chunking clean boundaries, and citations point to a meaningful file name.
- **Every file is dated** ("Last reviewed", "Status as of", or dated journal entries), so a model can tell which statement is newer.
- **Deliberate, realistic contradictions.** The October journal supersedes older notes: the editor changed from VS Code to Zed, and the sensor firmware changed from Rust to MicroPython at 30-minute intervals. This tests whether each configuration notices recency.
- **Explicit instructions for the assistant** (`communication_style.md`) so personalization can be checked, not just recall.
- **Sized on purpose.** About 22,000 characters, roughly 5,500 tokens. That fits easily in Gemini's window but exceeds Phi-4 Mini's default 4,096-token window, which demonstrates the context-stuffing limitation from Level 1.
- **Known gaps.** Nothing about movies or a desktop GPU, so absent-evidence questions have a correct answer of "not in the context".

## Reproduce

Follow Step 0 of `instructions.md` (Python 3.12 venv, Ollama with `phi4-mini:3.8b-q4_K_M` and `all-minilm`, `google-genai`, `GEMINI_API_KEY` set in the terminal). Then:

```bash
python run_comparison.py --prepare      # snapshot -> prepared_context/course.txt, build Chroma index
python run_comparison.py                # 12 questions x {Level 1, Level 2} x {Phi-4 Mini, Gemini}
python summarize_results.py             # writes evidence/RESULTS_SUMMARY.md
```

The scripts write their output into a local `evidence/` folder. In this repository, the contents of that folder were uploaded at the top level (`RESULTS_SUMMARY.md`, `results/`, `logs/`, `screenshots/`).

Useful options: `--only q01,q06`, `--levels 1`, `--dry-run`, `--delay 15` (if Gemini returns 429), and `--num-ctx 16384 --tag ctx16k` to rerun the local model with a larger context window.

Each level runs one `--compare` command, so Phi-4 Mini and Gemini receive the identical prompt (matching `prompt_sha256`). The runner adds no retries or fallbacks. Failed runs are recorded with their error and reported at the end.

## Note on .gitignore

The class `.gitignore` ignores `context_sample/`. In this repo it is tracked, because it is a synthetic persona and is a required deliverable. `prepared_context/`, `results/`, `local_vectordb/`, and the graph artifacts remain ignored.
