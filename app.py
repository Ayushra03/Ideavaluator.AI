import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st
import time

load_dotenv()

RESPONSE = """ """

def stream_data():
    for word in RESPONSE.split(" "):
        yield word + " "
        time.sleep(0.04)


genai.configure(api_key= os.environ.get("API_KEY"))

st.title("💡 Ideavalutor.AI", help="AI startup idea evaluator")
st.write("Before pitching your idea , let's have a quick evaluation using AI.")
st.write("Enter your idea")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", 
                            system_instruction="""You are an startup idea evaluator, who evaluates the young statup idea on the basis of market
                            that this idea will become a unicorn business or not.Consider the current business landscape and analyze whether the proposed idea aligns with existing successful ventures. If the idea introduces innovation, evaluate its potential to disrupt the market and create new opportunities. Provide insights on the market viability, scalability, competitive advantage, and potential challenges faced by the startup in achieving significant growth and becoming a sustainable, thriving business
                            , However if user asks any other thing that politely deny them telling them that I am an idea evaluator
                                            """)
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

chat = model.start_chat(history=st.session_state["chat_history"])

for msg in chat.history:
    st.chat_message(msg.role).write(msg.parts[0].text)

prompt = st.chat_input("Type your Idea here...")

if prompt:
    st.chat_message("user").write(prompt)
    response = chat.send_message(prompt)
    RESPONSE = response.text
    st.chat_message("🐯").write_stream(stream_data)
    st.session_state["chat_history"]=chat.history
