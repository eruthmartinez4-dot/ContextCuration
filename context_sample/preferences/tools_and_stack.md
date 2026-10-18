# Tools and Stack

Last reviewed: 2026-08-30

## Hardware

- Personal laptop: MacBook Air M3, 16 GB unified memory, 512 GB SSD. This is where I run Ollama and all coursework.
- Work laptop: Windows 11 Dell Latitude (locked down by IT; no local LLMs, no personal code).
- No dedicated GPU machine. For anything that needs a GPU I use a free-tier notebook service.

## Editors and terminals

- Editor: VS Code for everything (work and personal), with the Python, Ruff, and GitLens extensions.
- Terminal: iTerm2 with zsh on the Mac; PowerShell on the work laptop.

## Languages and libraries

- Python 3.12 is my main language. I use venv for environments (the class standard is .venv-mcp).
- Data: pandas, polars (learning), DuckDB for local analytics, SQL (PostgreSQL dialect at home, SQL Server at work).
- ML: scikit-learn, XGBoost, SHAP for explanations. I have used PyTorch only in tutorials.
- Retrieval and LLMs: Ollama (phi4-mini, all-minilm, llava), ChromaDB, the google-genai SDK for Gemini.
- Visualization: matplotlib and seaborn for notebooks; Tableau at work.

## Data and infrastructure

- PostgreSQL 16 running locally in Docker for personal projects.
- dbt Core at work for transformations (I maintain about 40 models in the member_insights project).
- GitHub for all personal repositories; I use Conventional Commits and small pull requests even on solo projects.

## Things I avoid

- Jupyter notebooks for anything that needs to be rerun regularly; I move logic into .py modules early.
- Cloud services that require a credit card for the free tier, unless the class requires them.
