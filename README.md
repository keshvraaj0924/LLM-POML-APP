> A comprehensive toolkit for comparing **Prompt Orchestration Markup Language (POML)** and **RAW prompt** performance with Large Language Models.

## 🎯 What This Project Does

This project provides **side-by-side comparison tools** to evaluate:
- **POML structured prompts** vs **RAW simple prompts**
- **Performance metrics** (processing speed, response quality)
- **Interactive chat interface** for real-time testing
- **CPU-optimized LLM inference** with local models

## 📁 Project Structure

llm-poml-app/
├── 📁 venv/ # Python virtual environment
├── 📁 poml_app/ # Main application
│ ├── 🐍 main.py # CLI comparison tool
│ ├── 🌐 streamlit_app.py # Web UI interface
│ ├── 🚀 launcher.py # Choose CLI or UI
│ ├── 📁 prompts/ # Template files
│ │ ├── chat.poml # POML templates
│ │ └── optimized_chat.poml # Optimized POML
│ └── 📁 services/ # Core modules
│ ├── ollama_client.py # LLM interface
│ └── poml_runner.py # Template processor
├── 📁 tests/ # Unit tests
├── 📋 requirements.txt # Dependencies
└── 📖 README.md # This file

## ✨ Key Features

### 🔄 **Dual Interface**
- **CLI Tool**: Fast command-line comparisons
- **Streamlit UI**: Interactive web interface with real-time metrics

### 📊 **Performance Analysis**
- **Processing Time**: POML template compilation vs RAW string formatting
- **LLM Inference**: Response generation time comparison
- **Quality Metrics**: Response structure and appropriateness analysis

### 🎛️ **Template Management**
- **Multiple POML Templates**: From complex to optimized versions
- **Smart RAW Templates**: Greeting detection and contextual responses
- **Easy Switching**: Compare different template approaches instantly

### 📈 **Detailed Metrics**
- Processing overhead calculation
- Response time breakdown
- Quality scoring system
- Performance trend analysis


## 🎮 How to Use

### **CLI Interface**
1. Run `python main.py`
2. Enter your query (e.g., "What is AI?")
3. See side-by-side comparison with metrics

### **Streamlit Interface**
1. Run `streamlit run streamlit_app.py`
2. Open browser to `http://localhost:8501`
3. Chat interface with real-time POML vs RAW comparison
4. Toggle metrics and template options in sidebar

## 📊 Performance Benchmarks

### Current Results (CPU Laptop)

|     Metric           | POML       | RAW      | Difference |
|--------------------- |------------|--------- |------------|
| **Processing Time**  |  3.6s      | 0.01s    | +360000%   |
| **LLM Inference**    |  2-4 min   | 1-2 min  | +50-100%   |
| **Total Overhead**   | +84-200%   | Baseline | Significant|
| **Response Quality** |  Excellent | Good     | POML wins  |


### 🤖 Model Setup

This project uses the **Mistral 7B model** via Ollama for local LLM inference.

**Why Mistral?**
- 🏠 **Runs locally** - No API keys or internet required
- ⚡ **CPU optimized** - Good performance on laptop hardware  
- 🎯 **Instruction tuned** - Perfect for prompt comparison tasks
- 📦 **Compact size** - 7B parameters, reasonable download/memory usage