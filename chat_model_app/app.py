import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from decouple import config

# openai_api_key = config('openai_api_key')
os.environ["OPENAI_API_KEY"] = config('openai_api_key')

st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("Demo chat GPT")

if "sessionMessages" not in st.session_state:
    st.session_state.sessionMessages = [
        SystemMessage(content="You are a helpful assistant")
    ]


def load_answer(question):
    st.session_state.sessionMessages.append(HumanMessage(content=question))
    assistant_answer = chat(st.session_state.sessionMessages)
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    return assistant_answer.content

def get_text():
    input_text = st.text_input("You: ", key=input)
    return input_text

chat = ChatOpenAI(temperature=0)


user_input=get_text()
submit = st.button('Generate')

if submit:
    response = load_answer(user_input)
    st.subheader("Answer:")
    st.write(response,key=1)
