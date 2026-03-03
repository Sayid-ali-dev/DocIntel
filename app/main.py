import os
import shutil
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from app.ingest import ingest_document
from app.retrieve import retrieve_chunks
from app.generate import generate_answer

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

class AskRequest(BaseModel):
    question: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def uplaod_document(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunk_count = ingest_document(temp_path, file.filename)

    os.remove(temp_path)

    return {
        "message": f"Document uploaded successfully",
        "filename": file.filename,
        "chunks_stored": chunk_count
    }

@app.post("/ask")
async def ask_questions(body: AskRequest):
    chunks = retrieve_chunks(body.question)
    result = generate_answer(body.question, chunks)

    return {
        "question": body.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }