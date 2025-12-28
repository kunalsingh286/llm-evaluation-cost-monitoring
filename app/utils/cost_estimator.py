MODEL_PRICING = {
    "tinyllama": {
        "input": 0.0001,   # simulated cost per token
        "output": 0.0002
    }
}

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model)

    if not pricing:
        return 0.0

    return round(
        (input_tokens * pricing["input"]) +
        (output_tokens * pricing["output"]),
        6
    )
