"""Run the fixed evaluation questions through Level 1 and Level 2 on both answer models.

Four configurations per question:
  Level 1 (no vector DB, full context stuffed)  x  {Phi-4 Mini (local), Gemini Flash}
  Level 2 (vector DB, top-k retrieved chunks)   x  {Phi-4 Mini (local), Gemini Flash}

Each level uses one --compare command, so both models in that level receive the
identical prompt (same prompt_sha256). Output streams to the terminal (good for
screenshots) and is also saved to evidence/logs/. JSON reports go to
evidence/results/. Then run summarize_results.py.

Examples:
  python run_comparison.py --prepare             # build snapshot + vector index first
  python run_comparison.py                       # all questions, both levels
  python run_comparison.py --only q01,q06 --levels 1
  python run_comparison.py --levels 1 --num-ctx 16384 --tag ctx16k   # optional: fix local overflow
  python run_comparison.py --dry-run             # print commands only
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

LOCAL_MODEL = "phi4-mini:3.8b-q4_K_M"
GEMINI_MODEL = "gemini-3.8-flash"
SNAPSHOT = Path("prepared_context/course.txt")


def run(cmd: list[str], log_path: Path | None, dry_run: bool) -> int:
    printable = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    print(f"\n$ {printable}", flush=True)
    if dry_run:
        return 0
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"}
    log = None
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log = log_path.open("w", encoding="utf-8")
        log.write(f"$ {printable}\n")
    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, encoding="utf-8", errors="replace", env=env) as proc:
            for line in proc.stdout:
                sys.stdout.write(line)
                if log:
                    log.write(line)
            return proc.wait()
    finally:
        if log:
            log.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--questions", type=Path, default=Path("eval/questions.json"))
    parser.add_argument("--only", help="Comma-separated question ids, e.g. q01,q06")
    parser.add_argument("--levels", default="1,2", help="Which levels to run: 1, 2, or 1,2")
    parser.add_argument("--out", type=Path, default=Path("evidence"))
    parser.add_argument("--tag", default="", help="Suffix for output folders, e.g. ctx16k")
    parser.add_argument("--local-model", default=LOCAL_MODEL)
    parser.add_argument("--gemini-model", default=GEMINI_MODEL)
    parser.add_argument("--top-k", type=int, default=3, help="Level 2 retrieved chunks")
    parser.add_argument("--num-ctx", type=int, help="Ollama context window (script default is 4096)")
    parser.add_argument("--delay", type=float, default=8.0,
                        help="Seconds to wait between commands to stay under Gemini free-tier RPM")
    parser.add_argument("--prepare", action="store_true",
                        help="Build prepared_context/course.txt and the vector index, then exit")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    py = sys.executable

    if args.prepare:
        steps = [
            [py, "level1_raw_context.py", "--folder", "context_sample",
             "--save-context", str(SNAPSHOT), "--prepare-only"],
            [py, "level2_vector_rag.py", "--folder", "prepared_context",
             "--db", "local_vectordb", "--index-only"],
        ]
        for step in steps:
            code = run(step, args.out / "logs" / "prepare.txt", args.dry_run)
            if code:
                print(f"\nPreparation failed (exit {code}). Fix the error above before continuing.")
                return code
        print("\nPrepared snapshot and vector index.")
        return 0

    if not args.dry_run:
        if not SNAPSHOT.exists():
            print(f"Missing {SNAPSHOT}. Run: python run_comparison.py --prepare")
            return 1
        if not os.environ.get("GEMINI_API_KEY", "").strip():
            print("GEMINI_API_KEY is not set in this terminal; Gemini runs will be recorded as errors.")

    questions = json.loads(args.questions.read_text(encoding="utf-8"))["questions"]
    if args.only:
        wanted = {q.strip() for q in args.only.split(",")}
        questions = [q for q in questions if q["id"] in wanted]
    levels = [lvl.strip() for lvl in args.levels.split(",") if lvl.strip()]
    suffix = f"-{args.tag}" if args.tag else ""
    compare = ["--compare", f"ollama={args.local_model}", "--compare", f"gemini={args.gemini_model}"]
    extra = ["--num-ctx", str(args.num_ctx)] if args.num_ctx else []

    failures = []
    total = len(questions) * len(levels)
    done = 0
    for q in questions:
        for level in levels:
            done += 1
            name = f"level{level}{suffix}"
            print(f"\n{'=' * 70}\n[{done}/{total}] {q['id']} ({q['category']}) | {name}\n"
                  f"Q: {q['question']}\n{'=' * 70}", flush=True)
            results = args.out / "results" / name / f"{q['id']}.json"
            if level == "1":
                cmd = [py, "level1_raw_context.py", "--context-file", str(SNAPSHOT)]
            elif level == "2":
                cmd = [py, "level2_vector_rag.py", "--skip-index", "--top-k", str(args.top_k)]
            else:
                print(f"Unknown level {level}; skipping.")
                continue
            cmd += ["--query", q["question"], *compare, *extra, "--results", str(results)]
            code = run(cmd, args.out / "logs" / name / f"{q['id']}.txt", args.dry_run)
            if code:
                failures.append(f"{q['id']} {name} (exit {code})")
            if done < total and not args.dry_run:
                time.sleep(args.delay)

    print(f"\nFinished {done} commands.")
    if failures:
        print("Some runs did not finish cleanly (check the logs and finish reasons):")
        for item in failures:
            print(f"  - {item}")
    print("Next: python summarize_results.py")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
