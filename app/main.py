from fastapi import FastAPI
from app.db.database import init_db
from app.services.llm_logger import log_llm_call
from app.services.regression_tester import compare_calls

app = FastAPI(title="LLM Evaluation & Cost Monitor")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/generate")
def generate(prompt: str, prompt_version: str = "v1"):
    return log_llm_call(prompt, prompt_version)

@app.post("/regression-test")
def regression_test(old_call_id: int, new_call_id: int):
    return compare_calls(old_call_id, new_call_id)

