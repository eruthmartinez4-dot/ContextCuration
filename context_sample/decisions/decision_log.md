# Decision Log

A record of decisions I made, with reasons, so I do not reargue them later.

## D-001 (2026-08-18): Use synthetic data for the capstone

Decision: Generate synthetic member data instead of using real or de-identified credit union data.
Reasons: Credit union privacy policy, the wish to publish the repository publicly, and avoiding a long approval process with compliance.
Trade-off accepted: Results will not prove real-world performance; the report must say so clearly.

## D-002 (2026-09-01): XGBoost before any deep learning

Decision: Use logistic regression and XGBoost for the capstone; no neural networks unless both fail badly.
Reasons: Tabular data, need for explanations that branch staff understand (SHAP), and I can train XGBoost on my laptop in minutes.

## D-003 (2026-10-06): Chroma instead of pgvector for class retrieval work

Decision: Use the local ChromaDB setup from the class scripts rather than adding the pgvector extension to my PostgreSQL container.
Reasons: The class scripts already use Chroma, setup is zero-configuration, and I do not need SQL joins with the vectors yet.
Revisit if: I want to store vectors next to capstone tables in PostgreSQL, or the collection grows beyond what a laptop handles comfortably.

## D-004 (2026-10-06): Keep personal context free of secrets

Decision: My curated context folder will never contain passwords, API keys, account numbers, health details, or real member information.
Reasons: The free tier of the Gemini API may use submitted content to improve products, and the folder is published on GitHub.
