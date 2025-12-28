from app.db.database import get_connection
from app.services.ollama_client import generate_response
from app.utils.token_counter import count_tokens
from app.utils.cost_estimator import estimate_cost

MODEL_NAME = "tinyllama"

def log_llm_call(prompt: str):
    response, latency_ms = generate_response(prompt)

    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(response)
    estimated_cost = estimate_cost(
        MODEL_NAME,
        input_tokens,
        output_tokens
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO llm_calls (
            prompt, response, model,
            input_tokens, output_tokens,
            estimated_cost, latency_ms
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            prompt,
            response,
            MODEL_NAME,
            input_tokens,
            output_tokens,
            estimated_cost,
            latency_ms
        )
    )

    conn.commit()
    conn.close()

    return {
        "prompt": prompt,
        "response": response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": estimated_cost,
        "latency_ms": latency_ms
    }

