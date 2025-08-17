from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from config.config_loader import load_config
from config.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
config = load_config()
logger = get_logger(__name__)

def create_embedder():
    model_name = config['embeddings']['model_name']
    logger.info(f'Creating HuggingFace endpoint embeddings for model: {model_name}')
    embedder = HuggingFaceEndpointEmbeddings(model=model_name)
    logger.info('Embedder created successfully')
    return embedder 