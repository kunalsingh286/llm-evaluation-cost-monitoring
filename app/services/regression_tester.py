from app.db.database import get_connection

def compare_calls(old_call_id: int, new_call_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT judge_score FROM evaluations WHERE llm_call_id = ?",
        (old_call_id,)
    )
    old_score = cursor.fetchone()["judge_score"]

    cursor.execute(
        "SELECT judge_score FROM evaluations WHERE llm_call_id = ?",
        (new_call_id,)
    )
    new_score = cursor.fetchone()["judge_score"]

    score_delta = new_score - old_score

    if score_delta > 0:
        verdict = "improved"
    elif score_delta < 0:
        verdict = "regressed"
    else:
        verdict = "no_change"

    cursor.execute(
        """
        INSERT INTO regressions (
            old_call_id,
            new_call_id,
            score_delta,
            verdict
        )
        VALUES (?, ?, ?, ?)
        """,
        (old_call_id, new_call_id, score_delta, verdict)
    )

    conn.commit()
    conn.close()

    return {
        "old_call_id": old_call_id,
        "new_call_id": new_call_id,
        "score_delta": score_delta,
        "verdict": verdict
    }
