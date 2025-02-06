import streamlit as st
import helper as gh

st.title("Groq Chatbot Application")

if "model_histories" not in st.session_state:
    st.session_state.model_histories = {}

if "selected_model" not in st.session_state:
    st.session_state.selected_model = 'gemma2-9b-it'

model_options=["gemma2-9b-it", "deepseek-r1-distill-llama-70b","mixtral-8x7b-32768"]
with st.sidebar:
    selected_model = st.selectbox("Select Model", model_options, index=model_options.index(st.session_state.selected_model))
    st.session_state.selected_model = selected_model 

if st.session_state.selected_model not in st.session_state.model_histories:
    st.session_state.model_histories[st.session_state.selected_model] = [
        {"role": "system", "content": "Welcome! Ask me anything, and I'll do my best to assist you."}
    ]

history=st.session_state.model_histories[st.session_state.selected_model]
for message in history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Enter your question here:")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    response, updated_history = gh.user_request(user_input, 
                                                   st.session_state.model_histories[st.session_state.selected_model],
                                                   st.session_state.selected_model)

    with st.chat_message("assistant"):
        st.write(response)
    
    st.session_state.model_histories[st.session_state.selected_model] = updated_history