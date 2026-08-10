# AI study features

## Flashcards

Flashcards are persisted in the dedicated `ai_learning.sqlite3` database. The selected course/module is the grounding scope. If no cards exist, the UI shows an explicit empty state and offers AI generation. Generated cards retain a SHA-256 hash of the authored grounding context for provenance.

## Intelligent assessments

A learner selects multiple modules from one course. The generated assessment mixes `multiple_choice` and `short_reasoning` items. The visible question never displays the source module. The source `module_id` is persisted in `generated_questions` for provenance and reinforcement analytics.

Multiple-choice answers are deterministic. Short reasoning answers are graded by the configured Ollama model against the generated reference answer and rubric. Every attempt updates module-level performance.

Reinforcement weights are computed per selected module:

- no history: neutral weight;
- accuracy below 50%: progressively higher weight;
- accuracy above 50%: progressively lower weight;
- weights are normalized across the selected modules.

The weight is sent to the generator as an instruction; it is not shown to the learner.

## Programming feedback

The programming tab uses authored `PracticeExercise` prompts and starter code. Submitted code is sent to the configured Ollama model with the exercise prompt. The response is schema-constrained and rendered in exactly four sections:

1. Corrección
2. Complejidad y eficiencia
3. Buenas prácticas
4. Sugerencia de mejora

The full source and structured feedback are persisted for later review.

## Persistence boundary

AI-generated learning artifacts live in `ai_learning.sqlite3` and are deliberately separated from deterministic mastery in `learning_progress.sqlite3`. AI observations and feedback therefore do not silently mutate official mastery state.

## Migration

The SQL contract is stored at `src/computational_biomedicine_study_hub/storage/migrations/004_ai_learning.sql`. The runtime migration is implemented by `AILearningStore` and uses SQLite `PRAGMA user_version`.
