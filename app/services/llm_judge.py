import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
JUDGE_MODEL = "tinyllama"

def judge_response(prompt: str, response: str) -> tuple:
    judge_prompt = f"""
You are an expert evaluator.

Score the following answer from 1 to 10 based on:
- correctness
- clarity
- completeness

Return ONLY in this format:
Score: <number>
Reason: <short explanation>

Question:
{prompt}

Answer:
{response}
"""

    payload = {
        "model": JUDGE_MODEL,
        "prompt": judge_prompt,
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=payload)
    res.raise_for_status()

    text = res.json()["response"]

    score = 0
    reason = text.strip()

    for line in text.splitlines():
        if "score" in line.lower():
            try:
                score = float(line.split(":")[-1].strip())
            except:
                score = 0

    score = max(0, min(score, 10))
    return score, reason
