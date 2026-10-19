from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
loader=DirectoryLoader(path="./guides",glob="**/*.pdf",loader_cls=PyPDFLoader)
raw_docs=loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
documents=text_splitter.split_documents(raw_docs)
embeddings=OllamaEmbeddings(model="mxbai-embed-large")

db_location="./chroma_db"
add_documents=not os.path.exists(db_location)
if  add_documents:
    vector_store=Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="moral_guides",
        persist_directory=db_location,
        )
else:
    vector_store=Chroma(
        collection_name="moral_guides",
        persist_directory=db_location,
        embedding_function=embeddings,
        )

    
    
    
retriver=vector_store.as_retriever(search_kwargs={"k":5})