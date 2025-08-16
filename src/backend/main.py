from fastapi import FastAPI, HTTPException
from pipeline.rag_pipeline import BudgetRAGInferencePipeline
from pydantic import BaseModel, Field
from config.logger import get_logger
import os

logger = get_logger(__name__)
app = FastAPI(title='PolicyRAG', description='RAG-Based Financial Assistant', version='0.1.0')

inference_pipeline = BudgetRAGInferencePipeline()
inference_pipeline.load_vectorstore()
inference_pipeline.create_qa_chain()

class QueryRequest(BaseModel):
    question: str = Field(..., description='Your question related to Budget 2025')

@app.get("/")
def intro():
    return {'message': 'This is your way to ask questions from Budget 2025'}

@app.post("/query")
def query_rag(query: QueryRequest):
    question = query.question
    if not question.strip():
        raise HTTPException(status_code=400, detail='Question cannot be empty')
    logger.info(f'Recieved Question: {question}')
    try:
        result = inference_pipeline.query(question)
        answer = result.get("answer")
        return {'question':question, 'answer':answer}   
    except Exception as e:
        logger.error(f"Error querying RAG pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))