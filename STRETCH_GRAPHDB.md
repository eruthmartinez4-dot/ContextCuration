# Stretch: When Does a Knowledge Graph Help, and When Is It a Waste of Compute?

This analysis is based on how this repository actually builds and queries its graph (`build_graph.py`, `graph_context.py`), applied to my curated context folder. Section 4 is where I record what happened when I tried it.

## 1. What the graph in this repo really is

- **Extraction** (`build_graph.py`): Gemini reads the prepared corpus in batches of about 6,000 characters. It returns `(subject, relation, object, quote)` triples, and every quote must appear verbatim in the source excerpt or the batch is rejected. The result is stored as a NetworkX `MultiDiGraph` in `local_graph.json`.
- **Cost for my corpus**: 14 source units pack into **5 batches, so 5 Gemini requests**, once. Successful batches are cached, so an unchanged rerun costs nothing.
- **Retrieval** (`graph_context.py`): no model call and no embeddings. Edges are ranked by **literal word overlap** between the question and the edge text and quotes (up to 12 edges), or filtered by an entity-name substring. There is no synonym or alias handling.
- **Freshness**: the graph is rejected as stale if any prepared file changes. Because batches are packed sequentially, an edit early in the corpus can shift later batch boundaries and trigger several new requests, not just one.

So the graph is not a smarter search engine. It is a precomputed index of **explicit, quote-backed relationships**, retrieved by keywords.

## 2. Where it should help

**Multi-hop and "who/what is connected to X" questions.** Question q10 ("everyone connected to my capstone") is spread across `people/collaborators.md` and `projects/capstone_member_churn.md`. Vector top-3 can easily return the two capstone chunks and miss Marcus Lee, whose connection is described in the people file. An entity filter such as `--entity "Member Churn"` returns every incident edge at once, regardless of which chunk mentions it.

**Aggregation across many files.** Questions like "every decision that involves PostgreSQL" or "everything that changed in October" pull facts from several documents. Vectors return the k most similar chunks. A graph returns all matching edges, up to its limit.

**Small local models with small context windows.** This matters most in this course. Phi-4 Mini has a 4,096-token window by default. A dozen compact triples with short quotes deliver dense, citable facts in a few hundred tokens. Stuffing 22,000 characters overflows, and three 600-character chunks may contain mostly irrelevant text.

**Keeping conflicting claims visible.** The extraction prompt preserves opposing claims as separate edges. For q06 and q07, both "uses VS Code" and "switched to Zed" may appear as edges with their quotes. That makes the contradiction visible to the answer model, provided the dates were captured in the relation or quote.

**Exposing structure through MCP (Level 5).** `get_relationships()` lets any host model ask structured questions about my context without the host having to read the files. That is useful when the host is a frontier model in another application.

## 3. Where it is likely a waste of compute

**Small corpora with a large-context frontier model.** My entire corpus is about 6,000 tokens. Gemini Flash can read all of it on every call (config C). Building a graph adds 5 extraction calls, another artifact to keep fresh, and another failure mode, for little gain in answer quality.

**Single-fact lookups and preferences.** For q01 to q03 (deadline, moisture threshold, "tl;dr" rule), one chunk contains the answer and vector search finds it. The graph adds nothing, and preference rules ("never use emojis") do not fit the subject-relation-object form well.

**Broad "key themes" questions.** The repo documents that broad questions with mostly stopwords return a bounded, deterministic sample, not a relevance-ranked survey. q12 is better served by stuffing or by vector retrieval with a higher top-k.

**Absent-evidence questions.** q08 (favorite movie) returns no edges. That is correct but costs nothing to get right without a graph either.

**Synonyms and paraphrase.** Retrieval is lexical. If I ask about my "advisor" but the edge says `faculty_advisor_of`, the match works. If I ask about my "mentor", it fails, while embedding search would probably succeed.

**Frequently changing personal notes.** Context that changes weekly (journal, schedule) keeps invalidating the graph, and each rebuild costs cloud calls. Vector re-indexing is local and free with `all-minilm`.

## 4. Status of my trial run

Not run yet. Building the graph needs Gemini, and my comparison run used up the free tier's daily limit of 20 requests (see `COMPARISON.md`). My comparison results already show where a graph could help: on q10, top-3 vector retrieval found at most 3 of the 4 people connected to the capstone, and on q07 it retrieved only the outdated garden-sensor file and missed the newer journal entry.

Planned commands once the quota resets (about 5 requests for this corpus):

```bash
python build_graph.py --folder prepared_context --graph local_graph.json
python level3_graph_rag.py --query "List every person connected to my capstone project and describe each person's role in it. Cite the sources."
python level4_hybrid_rag.py --query "List every person connected to my capstone project and describe each person's role in it. Cite the sources."
```

What I would check: whether the graph returns all four people for q10, whether it keeps both the old and new garden-sensor claims for q07, and whether it splits one person into several entities (for example "Priya Raman" and "Dr. Priya Raman").

## 5. Decision rule I would use

Build a graph when **all three** hold: the corpus is too large to stuff into the answer model's context, the important questions are about relationships between entities rather than single facts, and the corpus is stable enough that extraction cost is paid rarely. Otherwise, use context stuffing for small corpora with frontier models, and vector retrieval for everything else. For local SLMs, a graph (or hybrid, Level 4) is the most promising way to fit many relevant facts into a small window, provided extraction is done once by a stronger model.
