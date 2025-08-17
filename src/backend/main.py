from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from pipeline.rag_pipeline import BudgetRAGInferencePipeline
from pydantic import BaseModel, Field
from config.logger import get_logger
import os

logger = get_logger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: Loading models and pipeline")
    app.state.pipeline = BudgetRAGInferencePipeline()
    app.state.pipeline.load_vectorstore()
    app.state.pipeline.create_qa_chain()
    logger.info("Models and pipeline loaded successfully")
    yield
    logger.info('Application Shutdown')

app = FastAPI(title='PolicyRAG', description='RAG-Based Financial Assistant', version='0.1.0', lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str = Field(..., description='Your question related to Budget 2025')

@app.get("/")
def intro():
    return {'message': 'This is your way to ask questions from Budget 2025'}

@app.post("/query")
def query_rag(query: QueryRequest, request: Request):
    question = query.question
    if not question.strip():
        raise HTTPException(status_code=400, detail='Question cannot be empty')
    logger.info(f'Recieved Question: {question}')
    try:
        inference_pipeline = request.app.state.pipeline
        result = inference_pipeline.query(question)
        answer = result.get("answer")
        return {'question':question, 'answer':answer}   
    except Exception as e:
        logger.error(f"Error querying RAG pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))