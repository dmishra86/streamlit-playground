import streamlit as st
# from streamlit_chat import message
from st_chat_message import message
from langchain import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory)
import tiktoken # for text tokenization
from langchain.memory import (ConversationTokenBufferMemory, 
                              ConversationSummaryMemory, 
                              ConversationBufferWindowMemory)
import os
# from dotenv import load_dotenv

# load_dotenv()

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'API_key' not in st.session_state:
    st.session_state['API_key'] = ''


def get_response(userInput, api_key):
    if st.session_state['conversation'] is None:
        llm = OpenAI(temperature=0,
                     openai_api_key=api_key)

        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )
    response = st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)
    
    return response

st.set_page_config(page_title="chatGPT clone", page_icon=":robot_face")
st.markdown("<h1 style='text-align: center;'>'How can I assist you? </h1>", unsafe_allow_html=True)

st.sidebar.title("😄")
st.session_state['API_key'] = st.sidebar.text_input("What is your API Key?", type="password")
summarize_button = st.sidebar.button("Summarize the conversation", key="summarize")
if summarize_button:
    summarize_placeholder = st.sidebar.write("Nice chatting with you my friend: \n\n"+ st.session_state['conversation'].memory.buffer) 




response_container = st.container()
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("Your question goes here:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")
        if submit_button:
            st.session_state['messages'].append(user_input)
            model_response = get_response(user_input, st.session_state['API_key'])
            st.session_state['messages'].append(model_response)
            
            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if (i%2)==0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '_AI')

