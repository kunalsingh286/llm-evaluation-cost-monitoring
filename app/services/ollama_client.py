import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

def generate_response(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    start_time = time.time()
    response = requests.post(OLLAMA_URL, json=payload)
    latency_ms = (time.time() - start_time) * 1000

    response.raise_for_status()
    data = response.json()

    return data["response"], latency_ms
