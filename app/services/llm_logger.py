from app.db.database import get_connection
from app.services.ollama_client import generate_response
from app.utils.token_counter import count_tokens
from app.utils.cost_estimator import estimate_cost
from app.services.evaluation_logger import run_full_evaluation

MODEL_NAME = "tinyllama"

def log_llm_call(prompt: str, prompt_version: str = "v1"):
    response, latency_ms = generate_response(prompt)

    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(response)
    estimated_cost = estimate_cost(MODEL_NAME, input_tokens, output_tokens)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO llm_calls (
            prompt, prompt_version, response, model,
            input_tokens, output_tokens,
            estimated_cost, latency_ms
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            prompt,
            prompt_version,
            response,
            MODEL_NAME,
            input_tokens,
            output_tokens,
            estimated_cost,
            latency_ms
        )
    )

    llm_call_id = cursor.lastrowid
    conn.commit()
    conn.close()

    evaluation = run_full_evaluation(
        llm_call_id, prompt, response
    )

    return {
        "llm_call_id": llm_call_id,
        "prompt_version": prompt_version,
        **evaluation
    }

