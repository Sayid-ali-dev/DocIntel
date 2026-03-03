import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_answer(query: str, chunks:list):
    context = ""
    sources = []

    for i, chunk in enumerate(chunks):
        context += f"[{i + 1}] {chunk.page_content}\n\n"
        sources.append({
            "chunk_index": i + 1,
            "document_name": chunk.metadata.get("document_name", "unknown"),
            "page": chunk.metadata.get("page", 0) + 1,
            "content": chunk.page_content[:200]
        })

    prompt_template = PromptTemplate(
        input_variables = ["context", "questions"],
        template = """
You are a document analysis assistant. Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I could not find this information in the document."
Always cite which source number [1], [2], etc. you used to answer.

Context:
{context}

Question: {question}

Answer: """

    )

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = prompt_template.format(
        context= context,
        question= query,
    )

    response = llm.invoke(prompt)

    return {
        "answer":response.content,
        "sources": sources
    }

