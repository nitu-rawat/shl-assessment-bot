# Conversational SHL Assessment Recommender

A production-grade, state-free conversational agent built for the **AI Intern Role** at **SHL Labs**. The service guides recruiters from vague intent to a grounded shortlist of SHL individual test solutions through dialogue while strictly respecting the non-negotiable API schema and guarding against common LLM failure modes.

---

## 🚀 Core Features & Guardrails Covered

*   **100% Schema Compliance:** Fully valid responses matching the specified `ChatResponse` structure under all edge cases.
*   **Zero-Hallucination Guarantee:** Recommendations and links are strictly pulled from the internal `catalog.json` database.
*   **Context-Aware Dialogues:** Handles multi-turn refinements (e.g., handling mid-conversation constraints) and test comparisons without state loss.
*   **Strict Scope Execution:** Refuses off-topic questions, general recruitment/legal advice, and prompt injection attempts.
*   **Performance Metrics Minded:** Optimized to reply well within the 30-second timeout and target a high Mean Recall@10.

---

## 🛠️ Architecture & Tech Stack

*   **Framework:** FastAPI (Python 3.10+) — Selected for high performance, native async support, and structural Pydantic data validation.
*   **Server/Hosting:** Uvicorn + Render (Free Tier cold-start optimized).
*   **Data Structure:** Grounded JSON Catalog (`catalog.json`) holding filtered individual solutions with accurate product deep-links.

---

## 💻 Local Setup Instructions

Follow these steps to run this service locally on your computer:

### 1. Clone the repository and enter the directory
```bash
git clone [https://github.com/nitu-rawat/shl-assessment-bot.git](https://github.com/nitu-rawat/shl-assessment-bot.git)
cd shl-assessment-bot