from fastapi import FastAPI, UploadFile, File
from rag import vector_store, generate_answer
from utils import extract_text_from_pdf, chunk_text

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend running"}

# Upload resume


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    chunks = chunk_text(text)
    vector_store.add_texts(chunks)
    return {"message": "Resume processed"}

# Ask question


@app.get("/query")
def query_resume(question: str):
    answer = generate_answer(question)
    return {"answer": answer}
