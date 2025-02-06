# 🚀 Groq-Powered Multi-Model Chatbot Interface

A multi-model chatbot interface AI platform leveraging Groq's accelerated inference capabilities across multiple advanced language models through a Streamlit interface.

## Key Features
- Multi-model support with seamless switching between Gemma, Deepseek and Mixtral LLMs
- Persistent conversation history per model
- Streamlit-based interactive UI
- System prompt customization
- API key security through environment variables

## Installation
git clone https://github.com/pavangrandhi25/groq-chatbot.git
cd groq-chatbot

## Create a virtual environment 
python -m venv venv
venv\Scripts\activate

## Install dependencies
pip install -r requirements.txt

## Configuration
Create `.env` file:
    echo "groq_api_key=your_api_key_here" > .env

## Usage
streamlit run groq_app.py

## Supported Models
- Gemma2-9B-IT
- Deepseek-R1-Distill-Llama-70B 
- Mixtral-8x7B-32768

## 📚 Documentation
| Component       | Purpose                                  |
|-----------------|------------------------------------------|
| app.py          | Main UI and session management           |
| helper.py       | API communication and response handling  |
