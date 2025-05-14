import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os

st.set_page_config(page_title="Kazakhstan Constitution AI (Ollama)", layout="wide")
st.title("🇰🇿 Constitution AI Assistant (Powered by Ollama)")

llm = ChatOllama(model="llama3")
embedding = OllamaEmbeddings(model="nomic-embed-text")  

persist_dir = "chroma_db"
upload_dir = "temp_uploads"
os.makedirs(upload_dir, exist_ok=True)

@st.cache_resource
def init_vectorstore():
    return Chroma(embedding_function=embedding, persist_directory=persist_dir)

vectorstore = init_vectorstore()

uploaded_files = st.file_uploader(
    "📄 Upload Constitution or Related PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("📚 Processing documents..."):
        for file in uploaded_files:
            upload_path = os.path.join(upload_dir, file.name)
            with open(upload_path, "wb") as f:
                f.write(file.getbuffer())

            loader = PyPDFLoader(upload_path)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = splitter.split_documents(documents)

            vectorstore.add_documents(docs)
            os.remove(upload_path) 

        vectorstore.persist()  
        st.success("✅ Documents uploaded and indexed.")

query = st.text_input("💬 Ask a question about the Constitution or uploaded documents:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if query:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    result = qa.run(query)
    st.session_state.chat_history.append((query, result))

if st.session_state.chat_history:
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**AI:** {a}")
