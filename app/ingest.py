import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

def ingest_document(file_path: str, document_name:str):
    print(f"Loading Document: {document_name}")

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    print(f"Splitting into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        separators = ["\n\n", "\n", ".", " "]
    )
    chunks= splitter.split_documents(pages)

    for i, chunk in enumerate(chunks):
        chunk.metadata["document_name"] = document_name
        chunk.metadata["chunk_index"] = i

    print(f"Embedding and storing {len(chunks)} chunks...")

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        connection_string=DATABASE_URL,
        collection_name="docintel_docs",
        pre_delete_collection=False
    )

    print(f"Done. {len(chunks)} chunks stored.")
    return len(chunks)
