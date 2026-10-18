# Applied AI Systems Studio: My Notes

These are my own summaries of the Tuesday studio sessions.

## Week 3 (2026-09-15): Prompting fundamentals

- A prompt is a specification; vague prompts produce vague answers.
- Few-shot examples work best when they cover edge cases, not only typical cases.
- Asking the model to cite its sources makes hallucinations easier to spot but does not prevent them.

## Week 4 (2026-09-22): Local models with Ollama

- Small language models (SLMs) such as Phi-4 Mini run on a laptop and keep data local.
- Quantization (for example q4_K_M) trades a little quality for much lower memory use.
- Ollama's default context window in our scripts is 4,096 tokens, even though the model supports more. If the prompt is longer, content is cut and the model never sees it.

## Week 5 (2026-09-29): Context windows and tokens

- Tokens, not files or pages, are the real budget. Roughly 4 characters of English per token.
- "Context stuffing" means pasting everything into the prompt. It is simple and works when the corpus is small, but cost and latency grow with every request, and models can lose track of details in the middle of long prompts.
- Frontier models such as Gemini Flash have very large context windows, so stuffing works for longer, but you still pay for every input token on every call.

## Week 6 (2026-10-06): Context curation and retrieval

- Curated context means deliberately choosing, organizing, and dating the information an agent can use.
- Good curation habits: one topic per file, clear headings, explicit "last reviewed" dates, and no secrets.
- Retrieval-augmented generation (RAG) embeds chunks into vectors and only sends the most similar chunks to the model.
- RAG reduces prompt size but can miss information if the right chunk is not in the top-k results.
- Next weeks preview: knowledge graphs for relationships between entities, and MCP so other applications can query our context.

## Questions I still have

- How do you pick chunk size? The class default is 600 characters with 80 overlap.
- When does a knowledge graph help more than a better embedding model?
