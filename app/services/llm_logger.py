from app.db.database import get_connection
from app.services.ollama_client import generate_response

def log_llm_call(prompt: str):
    response, latency_ms = generate_response(prompt)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO llm_calls (prompt, response, model, latency_ms)
        VALUES (?, ?, ?, ?)
        """,
        (prompt, response, "tinyllama", latency_ms)
    )

    conn.commit()
    conn.close()

    return {
        "prompt": prompt,
        "response": response,
        "latency_ms": latency_ms
    }
