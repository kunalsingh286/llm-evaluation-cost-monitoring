from app.db.database import get_connection
from app.services.rule_evaluator import evaluate_response
from app.services.llm_judge import judge_response

def run_full_evaluation(llm_call_id: int, prompt: str, response: str):
    rule_score, rule_details = evaluate_response(prompt, response)
    judge_score, judge_reasoning = judge_response(prompt, response)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO evaluations (
            llm_call_id,
            rule_score,
            judge_score,
            judge_reasoning,
            details
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            llm_call_id,
            rule_score,
            judge_score,
            judge_reasoning,
            rule_details
        )
    )

    conn.commit()
    conn.close()

    return {
        "rule_score": rule_score,
        "rule_details": rule_details,
        "judge_score": judge_score,
        "judge_reasoning": judge_reasoning
    }

