import streamlit as st
import os
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from decouple import config
from langchain.document_loaders.csv_loader import CSVLoader

os.environ["OPENAI_API_KEY"] = config('openai_api_key')

load_dotenv()

st.set_page_config(page_title="Text Embeddings Demo App", page_icon=":robot:")
st.header("Text Embeddings Demo App using small set of sample data")

embeddings = OpenAIEmbeddings()

loader = CSVLoader(file_path='streamlit-playground/text_embeddings_app/myData.csv', csv_args={
    'delimiter':',',
    'quotechar':'"',
    'fieldnames':['Words']
})

data = loader.load()
print(data)

db = FAISS.from_documents(data, embeddings)


def get_text():
    input_text = st.text_input("You: ", key=input)
    return input_text


user_input=get_text()
submit = st.button('Find similar things')

if submit:
    docs = db.similarity_search(user_input)
    st.subheader("Top Matchers:")
    st.text(docs[0].page_content)
    st.text(docs[1].page_content)

