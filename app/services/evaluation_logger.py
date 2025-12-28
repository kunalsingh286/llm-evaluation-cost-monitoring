from app.db.database import get_connection
from app.services.rule_evaluator import evaluate_response

def run_rule_evaluation(llm_call_id: int, prompt: str, response: str):
    score, details = evaluate_response(prompt, response)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO evaluations (llm_call_id, rule_score, details)
        VALUES (?, ?, ?)
        """,
        (llm_call_id, score, details)
    )

    conn.commit()
    conn.close()

    return score, details
