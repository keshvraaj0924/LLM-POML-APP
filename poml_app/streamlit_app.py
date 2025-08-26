import streamlit as st
import time
import sys
import os

# Add services to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.poml_runner import POMLRunner
from services.ollama_client import OllamaClient

# Initialize clients
@st.cache_resource
def get_ollama_client():
    return OllamaClient(model="mistral")

ollama = get_ollama_client()

# Page config
st.set_page_config(
    page_title="POML vs RAW Chat Comparison",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 POML vs RAW Template Comparison")
st.markdown("Compare responses from POML and RAW templates side by side")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    template_choice = st.selectbox(
        "POML Template",
        ["prompts/chat.poml", "prompts/elaborate_optimized_chat.poml"],
        help="Choose which POML template to use"
    )
    
    show_metrics = st.checkbox("Show Performance Metrics", value=True)
    show_prompts = st.checkbox("Show Generated Prompts", value=False)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper functions
def get_smart_raw_prompt(user_input: str) -> str:
    greetings = ['hi', 'hello', 'hey', 'sup', 'good morning']
    user_lower = user_input.lower().strip()
    is_greeting = any(greeting in user_lower for greeting in greetings) and len(user_input.split()) <= 3
    
    if is_greeting:
        return f"""You are a friendly assistant. The user said: '{user_input}' - respond with a brief, friendly greeting and ask how you can help."""
    else:
        return f"""You are a helpful assistant. Answer this question clearly: {user_input}"""

def process_query(user_input: str):
    results = {}
    
    # POML Processing
    with st.spinner("🔄 Processing POML..."):
        poml_start = time.time()
        try:
            poml_prompt = POMLRunner.run_prompt(template_choice, user_input=user_input)
            poml_process_time = time.time() - poml_start
            
            llm_start = time.time()
            poml_response = ollama.query(poml_prompt)
            poml_llm_time = time.time() - llm_start
            
            results['poml'] = {
                'prompt': poml_prompt,
                'response': poml_response,
                'process_time': poml_process_time,
                'llm_time': poml_llm_time,
                'total_time': poml_process_time + poml_llm_time
            }
        except Exception as e:
            results['poml'] = {'error': str(e)}
    
    # RAW Processing
    with st.spinner("🔄 Processing RAW..."):
        raw_start = time.time()
        raw_prompt = get_smart_raw_prompt(user_input)
        raw_process_time = time.time() - raw_start
        
        llm_start = time.time()
        raw_response = ollama.query(raw_prompt)
        raw_llm_time = time.time() - llm_start
        
        results['raw'] = {
            'prompt': raw_prompt,
            'response': raw_response,
            'process_time': raw_process_time,
            'llm_time': raw_llm_time,
            'total_time': raw_process_time + raw_llm_time
        }
    
    return results

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            # Display comparison results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏗️ POML Response")
                if 'error' in message["poml"]:
                    st.error(f"❌ POML Error: {message['poml']['error']}")
                else:
                    st.markdown(message["poml"]["response"])
                    
                    if show_metrics:
                        st.markdown("**📊 POML Metrics:**")
                        st.markdown(f"- Processing: {message['poml']['process_time']*1000:.1f}ms")
                        st.markdown(f"- LLM Time: {message['poml']['llm_time']*1000:.1f}ms")
                        st.markdown(f"- Total: {message['poml']['total_time']*1000:.1f}ms")
            
            with col2:
                st.markdown("### 📝 RAW Response")
                st.markdown(message["raw"]["response"])
                
                if show_metrics:
                    st.markdown("**📊 RAW Metrics:**")
                    st.markdown(f"- Processing: {message['raw']['process_time']*1000:.1f}ms")
                    st.markdown(f"- LLM Time: {message['raw']['llm_time']*1000:.1f}ms")
                    st.markdown(f"- Total: {message['raw']['total_time']*1000:.1f}ms")
            
            # Performance comparison
            if show_metrics and 'error' not in message["poml"]:
                st.markdown("---")
                poml_total = message["poml"]["total_time"] * 1000
                raw_total = message["raw"]["total_time"] * 1000
                overhead = ((poml_total - raw_total) / raw_total) * 100 if raw_total > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("POML Total", f"{poml_total:.1f}ms")
                with col2:
                    st.metric("RAW Total", f"{raw_total:.1f}ms")
                with col3:
                    st.metric("Overhead", f"{overhead:+.1f}%")

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process and display response
    with st.chat_message("assistant"):
        results = process_query(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "poml": results["poml"],
            "raw": results["raw"]
        })
        st.rerun()
