# main.py - Modified for real-time metrics
import time

from poml_app.services.poml_runner import POMLRunner
from poml_app.services.ollama_client import OllamaClient

ollama = OllamaClient(model="mistral")

def run_chat_with_metrics(user_input: str) -> str:
    # Start timing
    total_start = time.time()
    
    # POML processing time
    poml_start = time.time()
    filled = POMLRunner.run_prompt("poml_app/prompts/chat.poml", user_input=user_input)
    poml_end = time.time()
    
    # LLM inference time
    llm_start = time.time()
    response = ollama.query(filled)
    llm_end = time.time()
    
    # Calculate metrics
    total_time = llm_end - total_start
    poml_time = poml_end - poml_start
    llm_time = llm_end - llm_start
    
    # Display metrics
    print(f"\n📊 Query Metrics:")
    print(f"   POML Processing: {poml_time*1000:.1f}ms")
    print(f"   LLM Inference:   {llm_time*1000:.1f}ms") 
    print(f"   Total Time:      {total_time*1000:.1f}ms")
    print(f"   Prompt Length:   {len(filled)} chars")
    print(f"   Response Length: {len(response)} chars")
    print(f"   Overhead:        {(poml_time/total_time)*100:.1f}%")
    
    return response

if __name__ == "__main__":
    while True:
        user_input = input("\nAsk me something: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        
        response = run_chat_with_metrics(user_input)
        print(f"\n🤖 Response: {response}")
