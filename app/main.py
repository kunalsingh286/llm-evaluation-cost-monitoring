from fastapi import FastAPI
from app.services.llm_logger import log_llm_call
from app.db.database import init_db

app = FastAPI(title="LLM Evaluation & Cost Monitor")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/generate")
def generate(prompt: str):
    return log_llm_call(prompt)
