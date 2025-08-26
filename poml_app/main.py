# main.py - With POML vs RAW comparison
import time
from services.poml_runner import POMLRunner
from services.ollama_client import OllamaClient

ollama = OllamaClient(model="mistral")

def run_chat_with_poml(user_input: str) -> dict:
    """Run chat using POML with detailed metrics"""
    total_start = time.time()
    
    # POML processing time
    poml_start = time.time()
    filled = POMLRunner.run_prompt("prompts/chat.poml", user_input=user_input)
    poml_end = time.time()
    
    # LLM inference time
    llm_start = time.time()
    response = ollama.query(filled)
    llm_end = time.time()
    
    # Calculate metrics
    total_time = llm_end - total_start
    poml_time = poml_end - poml_start
    llm_time = llm_end - llm_start
    
    return {
        'method': 'POML',
        'response': response,
        'total_time': total_time,
        'processing_time': poml_time,
        'llm_time': llm_time,
        'prompt_used': filled,
        'prompt_length': len(filled),
        'response_length': len(response)
    }

def run_chat_with_raw(user_input: str) -> dict:
    """Run chat using smart RAW prompt with detailed metrics"""
    total_start = time.time()
    
    # Processing time start
    process_start = time.time()
    
    # Check if input is a greeting
    greetings = ['hi', 'hello', 'hey', 'sup', "what's up", 'good morning', 
                'good afternoon', 'good evening', 'how are you', 'howdy']
    
    user_lower = user_input.lower().strip()
    is_greeting = any(greeting in user_lower for greeting in greetings) and len(user_input.split()) <= 3
    
    if is_greeting:
        raw_prompt = f"""You are a friendly, helpful assistant.

The user has sent a greeting: "{user_input}"

Respond with a warm, friendly greeting and ask how you can help them today.
Keep your response brief and welcoming (1-2 sentences maximum).
Do not provide structured analysis or detailed explanations.
"""
    else:
        raw_prompt = f"""You are an expert assistant with expertise across multiple domains. 
Your responses should be comprehensive, well-structured, and educational.

Analyze the user's question: "{user_input}" and provide a thorough, educational response.

Follow these guidelines:
- Use clear, professional language appropriate for the topic complexity
- Include at least 2-3 specific examples when relevant
- Provide actionable insights or recommendations
- Aim for educational value while remaining engaging
- Keep each section focused and well-organized
- Target approximately 300-500 words for comprehensive coverage

Please structure your response as follows:

**Direct Answer:** [Provide a concise, direct answer to the question]

**Explanation:** [Give detailed context, background, and how/why information]

**Examples:** [Include 2-3 relevant, specific examples or use cases]

**Additional Insights:** [Offer valuable recommendations, tips, or related considerations]

**Summary:** [Conclude with 1-2 sentences capturing the key takeaway]

Use professional language while maintaining clarity and educational value.
"""
    
    # Processing time end
    process_end = time.time()
    processing_time = process_end - process_start
    
    # LLM inference time
    llm_start = time.time()
    response = ollama.query(raw_prompt)
    llm_end = time.time()
    
    total_time = time.time() - total_start
    llm_time = llm_end - llm_start
    
    return {
        'method': 'RAW',
        'response': response,
        'total_time': total_time,
        'processing_time': processing_time,
        'llm_time': llm_time,
        'prompt_used': raw_prompt,
        'prompt_length': len(raw_prompt),
        'response_length': len(response)
    }


def compare_approaches(user_input: str):
    """Compare POML vs RAW approaches side by side"""
    
    print(f"\n{'='*60}")
    print(f"🔬 TESTING QUERY: '{user_input}'")
    print(f"{'='*60}")
    
    # Test POML approach
    print("\n🔄 Running POML approach...")
    poml_result = run_chat_with_poml(user_input)
    
    print("\n🔄 Running RAW approach...")
    raw_result = run_chat_with_raw(user_input)
    
    # Display detailed comparison
    print_comparison_results(poml_result, raw_result)
    
    return poml_result, raw_result

def print_comparison_results(poml_result: dict, raw_result: dict):
    """Print detailed comparison between POML and RAW results"""
    
    print(f"\n{'='*60}")
    print("📊 PERFORMANCE COMPARISON")
    print(f"{'='*60}")
    
    # Timing comparison
    print(f"\n⏱️  TIMING BREAKDOWN:")
    print(f"{'Metric':<20} {'POML':<12} {'RAW':<12} {'Difference':<15}")
    print("-" * 60)
    
    # Processing time
    poml_proc = poml_result['processing_time'] * 1000
    raw_proc = raw_result['processing_time'] * 1000
    proc_diff = poml_proc - raw_proc
    print(f"{'Processing':<20} {poml_proc:>8.1f}ms {raw_proc:>8.1f}ms {proc_diff:>+8.1f}ms")
    
    # LLM inference time
    poml_llm = poml_result['llm_time'] * 1000
    raw_llm = raw_result['llm_time'] * 1000
    llm_diff = poml_llm - raw_llm
    print(f"{'LLM Inference':<20} {poml_llm:>8.1f}ms {raw_llm:>8.1f}ms {llm_diff:>+8.1f}ms")
    
    # Total time
    poml_total = poml_result['total_time'] * 1000
    raw_total = raw_result['total_time'] * 1000
    total_diff = poml_total - raw_total
    print(f"{'Total Time':<20} {poml_total:>8.1f}ms {raw_total:>8.1f}ms {total_diff:>+8.1f}ms")
    
    # Performance impact
    overhead_percent = (total_diff / raw_total) * 100 if raw_total > 0 else 0
    print(f"\n💡 PERFORMANCE IMPACT:")
    print(f"   POML Overhead: {total_diff:+.1f}ms ({overhead_percent:+.1f}%)")
    
    if overhead_percent > 5:
        print("   ❌ POML adds significant overhead")
    elif overhead_percent > 0:
        print("   ⚠️  POML adds minor overhead")
    else:
        print("   ✅ POML is comparable or faster")
    
    # Prompt analysis
    print(f"\n📝 PROMPT ANALYSIS:")
    print(f"   POML Prompt Length: {poml_result['prompt_length']} characters")
    print(f"   RAW Prompt Length:  {raw_result['prompt_length']} characters")
    print(f"   Length Difference:  {poml_result['prompt_length'] - raw_result['prompt_length']:+d} characters")
    
    # Response analysis
    print(f"\n💬 RESPONSE ANALYSIS:")
    print(f"   POML Response: {poml_result['response_length']} characters")
    print(f"   RAW Response:  {raw_result['response_length']} characters")
    print(f"   Length Diff:   {poml_result['response_length'] - raw_result['response_length']:+d} characters")
    
    # Show actual prompts (first 200 chars)
    print(f"\n📋 PROMPTS USED:")
    print(f"   POML Generated: {repr(poml_result['prompt_used'][:200])}...")
    print(f"   RAW Prompt:     {repr(raw_result['prompt_used'][:200])}...")
    
    # Show responses (first 100 chars)
    print(f"\n🤖 RESPONSES:")
    print(f"   POML: {poml_result['response'][:100]}...")
    print(f"   RAW:  {raw_result['response'][:100]}...")

def interactive_comparison():
    """Interactive mode for testing queries"""
    print("🔬 POML vs RAW Comparison Tool")
    print("Type 'quit' to exit, 'batch' for batch testing")
    
    while True:
        user_input = input("\n🎯 Enter query to test: ")
        
        if user_input.lower() in ['quit', 'exit']:
            break
        elif user_input.lower() == 'batch':
            run_batch_tests()
            continue
        
        compare_approaches(user_input)

def run_batch_tests():
    """Run predefined batch tests"""
    test_queries = [
        "hi",
        "What is AI?",
        "Explain machine learning in simple terms",
        "Tell me about the weather today",
        "How do neural networks work?"
    ]
    
    print(f"\n🔄 Running batch tests with {len(test_queries)} queries...")
    
    all_results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*20} Test {i}/{len(test_queries)} {'='*20}")
        poml_result, raw_result = compare_approaches(query)
        all_results.append((query, poml_result, raw_result))
    
    # Summary statistics
    print_batch_summary(all_results)

def print_batch_summary(results):
    """Print summary of batch test results"""
    print(f"\n{'='*60}")
    print("📈 BATCH TEST SUMMARY")
    print(f"{'='*60}")
    
    total_queries = len(results)
    total_poml_time = sum(r[1]['total_time'] for r in results)
    total_raw_time = sum(r[2]['total_time'] for r in results)
    total_poml_proc = sum(r[1]['processing_time'] for r in results)
    
    avg_poml_time = total_poml_time / total_queries
    avg_raw_time = total_raw_time / total_queries
    avg_poml_proc = total_poml_proc / total_queries
    
    print(f"\n📊 AVERAGES ACROSS {total_queries} QUERIES:")
    print(f"   Average POML Total Time: {avg_poml_time*1000:.1f}ms")
    print(f"   Average RAW Total Time:  {avg_raw_time*1000:.1f}ms")
    print(f"   Average POML Processing: {avg_poml_proc*1000:.1f}ms")
    print(f"   Average Overhead:        {((avg_poml_time - avg_raw_time)/avg_raw_time)*100:+.1f}%")
    
    # Consistency analysis
    poml_times = [r[1]['total_time'] for r in results]
    raw_times = [r[2]['total_time'] for r in results]
    
    import statistics
    poml_std = statistics.stdev(poml_times) if len(poml_times) > 1 else 0
    raw_std = statistics.stdev(raw_times) if len(raw_times) > 1 else 0
    
    print(f"\n📏 CONSISTENCY:")
    print(f"   POML Time Std Dev: {poml_std*1000:.1f}ms")
    print(f"   RAW Time Std Dev:  {raw_std*1000:.1f}ms")

if __name__ == "__main__":
    interactive_comparison()
