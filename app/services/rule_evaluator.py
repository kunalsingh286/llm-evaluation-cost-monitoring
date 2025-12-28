def evaluate_response(prompt: str, response: str) -> tuple:
    score = 0
    details = []

    # Rule 1: Non-empty response
    if response and response.strip():
        score += 2
        details.append("Non-empty response")
    else:
        details.append("Empty response")

    # Rule 2: Minimum length
    if len(response.split()) >= 10:
        score += 2
        details.append("Sufficient length")

    # Rule 3: Keyword relevance
    keywords = prompt.lower().split()
    match_count = sum(1 for k in keywords if k in response.lower())

    if match_count >= 2:
        score += 4
        details.append("Keyword relevance detected")

    # Rule 4: Repetition penalty
    words = response.lower().split()
    if len(words) != len(set(words)):
        score -= 2
        details.append("Repetition detected")

    score = max(0, min(score, 10))

    return score, ", ".join(details)
