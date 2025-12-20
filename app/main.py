from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.mongo import mongo_client
from app.api.routes import llmrequest
from app.api.routes import chatbot
from app.api.routes import insert_kb_item

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("connecting to db")
    mongo_client.connect()
    yield
    print("shutting down the connection")
    mongo_client.close()

app = FastAPI(title="RAG Chatbot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llmrequest.router)
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot Management"])
app.include_router(insert_kb_item.router, prefix="/api", tags=["Insert KB Item"])

@app.get("/")
async def root():
    return {"message": "Chatbot API Çalışıyor! 🚀"}