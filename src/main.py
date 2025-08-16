from pipeline.rag_pipeline import BudgetRAGInferencePipeline, BudgetRAGTrainingPipeline
from config.logger import get_logger
import os

logger = get_logger(__name__)

training_pipeline = BudgetRAGTrainingPipeline()
if not os.path.exists(training_pipeline.vectorstore_dir):
    retriever = training_pipeline.build_vectorstore()
else:
    print("Vector store already exists, skipping training.")
inference_pipeline = BudgetRAGInferencePipeline()
inference_pipeline.load_vectorstore()               
inference_pipeline.create_qa_chain()

question = "What are the income tax slabs in budget 2025?"
result = inference_pipeline.query(question)
print(result['answer'])