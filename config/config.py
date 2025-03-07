import os
from dotenv import load_dotenv
load_dotenv()


#Configuration setup for Concept Validation
GPT4O_MINI_CONFIG = {
    "OPENAI_API_KEY_4o_MINI": os.getenv("OPENAI_API_KEY_4o_MINI"),
    "OPENAI_ENDPOINT_4o_MINI": os.getenv("OPENAI_ENDPOINT_4o_MINI"),
    "TEMPERATURE" : 0,
    "MAX_RETRIES" : 5,
    'DEPLOYMENT' : 'gpt-4o-mini',
    'API_VERSION' : '2024-02-15-preview'
}

#Configuration setup for ChromaDB
CHROMA_DB_CONFIG = {
    "CHROMA_HOST": os.getenv("CHROMA_HOST"),
    "CHROMA_PORT": os.getenv("CHROMA_PORT"),
    "CHROMA_PROJECT_NAME": os.getenv("CHROMA_PROJECT_NAME")
}