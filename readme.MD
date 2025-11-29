
# 🤖 AI Chatbot Backend (RAG Architecture)

This project is a high-performance, asynchronous AI chatbot backend built with **FastAPI**. Currently, it integrates with **Google Gemini (2.0 Flash)** for LLM capabilities.

The project is designed with a **Modular Architecture** to support future expansions like Conversation Memory (MongoDB) and Retrieval-Augmented Generation (RAG) with Milvus.

## 🚀 Features (Current Status)

- **FastAPI Framework:** Fully asynchronous endpoints for high throughput.
- **Google Gemini Integration:** Uses the latest `google-genai` SDK (v1.0) with access to `gemini-2.0-flash`.
- **Structured Data:** Strict Request/Response validation using **Pydantic** models.
- **Traceability:** Unique IDs for requests, responses, and conversation sessions.
- **Environment Management:** Secure configuration using `.env` files.
- **Test Interface:** A simple, dark-mode HTML frontend for testing the API.

## 🗺️ Roadmap (Upcoming Features)

- [ ] **Conversation Memory:** Integration with **MongoDB** to store chat history and provide context-aware responses.
- [ ] **RAG Implementation:** Integration with **Milvus** vector database to answer questions based on specific documents.
- [ ] **Data Ingestion Pipeline:** Endpoints to upload and process PDF/Text documents (Chunking & Embedding).
- [ ] **Dockerization:** Full container support with Docker Compose.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **LLM Provider:** Google Gemini API
- **Utilities:** Pydantic, Python-Dotenv, Uvicorn

## 📂 Project Structure

```text
app/
├── api/
│   └── routes/         # API Endpoints (The "Waiter")
├── core/
│   ├── config.py       # Configuration management
│   └── constants.py    # Static variables
├── models/             # Pydantic Schemas (Request/Response)
├── services/           # Business Logic (The "Chef")
└── main.py             # Application Entry Point
```

## ⚡ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/kerimkaraman/simple_chatbot_with_rag.git
cd simple_chatbot_with_rag
```

### 2. Install Dependencies
Make sure you have Python installed. It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your Google API Key:

```ini
# .env file
GOOGLE_API_KEY=AIzaSxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=simple_chatbot_local
MONGO_CHAT_COLLECTION=conversations
```

### 4. Run the Server
Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```
*The API will start at `http://127.0.0.1:8000`*

### 5. Test the Chatbot
Open the `index.html` file in your browser to start chatting with the bot via the test interface.

Or access the Swagger UI documentation at:
`http://127.0.0.1:8000/docs`

---

## 🤝 Contributing
This project is currently under active development. Suggestions and Pull Requests are welcome!

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)

---