## 🚀 Technical Implementation & Design Decisions

This language feedback API was built with a focus on reliability, type safety, and clean architecture:

* **FastAPI & Uvicorn:** Chosen for high performance and asynchronous handling of AI API calls.
* **OpenAI Structured Outputs:** Utilized the `gpt-4o-mini` model with strict Pydantic models (`FeedbackResponse`) via the `.parse()` method. This guarantees 100% predictable JSON schemas and eliminates the risk of string-parsing errors.
* **Modular Architecture:** Separated routing (`main.py`), core logic (`feedback.py`), and data schemas (`models.py`) to maintain a clean separation of concerns.
* **Containerization:** Fully Dockerized using `python:3.11-slim` for a lightweight, reproducible environment that runs cleanly via `docker compose`.

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Akash17891234/intern-task-2026.git](https://github.com/Akash17891234/intern-task-2026.git)
   cd intern-task-2026