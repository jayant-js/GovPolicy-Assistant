from pipeline.rag_pipeline import BudgetRAGPipeline
from config.logger import get_logger

logger = get_logger(__name__)

pipeline = BudgetRAGPipeline()
pipeline.build_vectorstore()
pipeline.create_qa_chain()

question = "What are the income tax slabs in Budget 2025?"
result = pipeline.query(question)   

print(result['answer'])