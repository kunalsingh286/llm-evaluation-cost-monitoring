def count_tokens(text: str) -> int:
    """
    Approximate token count.
    1 token ≈ 4 characters (rough industry heuristic)
    """
    if not text:
        return 0
    return max(1, len(text) // 4)
