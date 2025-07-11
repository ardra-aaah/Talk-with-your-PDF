import streamlit as st
import os
import getpass
import time
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.vectorstores import InMemoryVectorStore
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma


template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""
if not os.environ.get("MISTRAL_API_KEY"):
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("<API KEY> ")

pdfs_directory = './pdf/'

embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory='./Chroma-DB'
)

from langchain_mistralai import ChatMistralAI

model =  ChatMistralAI(
    model = 'mistral-small-latest',
    mistral_api_key = os.environ["MISTRAL_API_KEY"],
    temperature=0
)

def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def index_docs(all_splits):
    """
    Indexes the document chunks into the vector store in batches.
    """
    for i in range(0, len(all_splits), 10):
        batch = all_splits[i : i + 10]
        vector_store.add_documents(documents=batch)
        print(f"Added documents {i}-{i + len(batch)}")
        time.sleep(3)
        

def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    return chain.invoke({"question": question, "context": context})

print("-"*30)
if "uploaded_file" in st.session_state:
    st.write("File indexed successfully, ask your questions now!")
else:
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf",
        accept_multiple_files=False
    )
    if uploaded_file:
        with st.spinner("Indexing...", show_time=True):
            upload_pdf(uploaded_file)
            documents = load_pdf(pdfs_directory + uploaded_file.name)
            chunked_documents = split_text(documents)
            index_docs(chunked_documents)
            st.session_state.uploaded_file = uploaded_file

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input("Ask your question")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        related_documents = retrieve_docs(prompt)
        print('related_documents: ', related_documents)
        answer = answer_question(prompt, related_documents)
        full_response = answer.content
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
