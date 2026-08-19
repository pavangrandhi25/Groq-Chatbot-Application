from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['groq_api']=os.getenv('groq_api_key')

client = Groq()

def user_request(user_input, chat_history,model_name):
    temp_chat_history =  [{"role": "system", "content": f"You are {model_name}, a powerful AI model. Answer queries accurately."}
    ] + chat_history + [{"role": "user", "content": user_input}]

    response = client.chat.completions.create(model=model_name, messages=temp_chat_history)

    assistant_response = response.choices[0].message.content

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response, chat_history



