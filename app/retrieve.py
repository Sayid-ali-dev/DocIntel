import os 
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector

load_dotenv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

def retrieve_chunks(query: str, k: int = 5):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectorstore = PGVector(
        connection_string=DATABASE_URL,
        embedding_function=embeddings,
        collection_name="docintel_docs"
    )

    results = vectorstore.similarity_search(query, k=k)

    return results