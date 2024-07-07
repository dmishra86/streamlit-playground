import streamlit as st
from utils import query_agent
from dotenv import load_dotenv

load_dotenv()

st.title("Data analysis tool - CSV file")
st.header(" Upload your CSV file:")

data = st.file_uploader("Upload CS file", type="csv")

query = st.text_area("Enter your query:")
button = st.button("Generate response")

if button:
    # get response
    answer = query_agent(data, query)
    st.write(answer)
    
