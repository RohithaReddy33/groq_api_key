import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

#load Environment variables
load_dotenv()
api_key = os.getenv("GROG_API_KEY")
client = Groq(api_key=api_key)

#streamlit page config
st.set_page_config(
    page_title="Groq API chatbot",
    page_icon="",
    layout="wide"
)

#title
st.title("Groq API chatbot")
st.write("powered by Groq llama model")

#sidebar
st.sidebar.title("Settings")
model=st.sidebar.selectbox("choose model",["llama-3.3-70b-versatile","llama-3.1-8b-instant"])
temperature=st.sidebar.slider("temperature",0.0,1.0,0.7)
max_tokens=st.sidebar.slider("max tokens",100,2024,1024)
if st.sidebar.button("clear chat"):
    st.session_state["messages"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = []

#display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input
prompt=st.chat_input("Ask me anything")
if prompt:
    st.session_state.messages.append({"role": "user", "content": "prompt"})
    with st.chat_message("user"):
        st.markdown(prompt)

    #display assistant response
    with st.chat_message("assistant"):
        with st.spinner("typing..."):
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})