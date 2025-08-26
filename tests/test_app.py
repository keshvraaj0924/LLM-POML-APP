# tests/test_app.py
import time
from poml_app.services.ollama_client import OllamaClient
from poml_app.services.poml_runner import POMLRunner

ollama = OllamaClient("mistral")

def benchmark(prompt_file, **kwargs):
    filled = POMLRunner.run_prompt(prompt_file, **kwargs)
    start = time.time()
    response = ollama.query(filled)
    end = time.time()
    return response, round(end - start, 2)

if __name__ == "__main__":
    # Benchmark with POML
    resp_poml, t1 = benchmark("poml_app/prompts/chat.poml", user_input="Tell me about AI")
    print(f"[POML] {resp_poml} (Time: {t1}s)")

    # Benchmark with RAW prompt
    start = time.time()
    resp_raw = ollama.query("Tell me about AI")
    end = time.time()
    print(f"[RAW] {resp_raw} (Time: {round(end - start, 2)}s)")
