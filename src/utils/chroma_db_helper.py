import os
import chromadb
from dotenv import load_dotenv
from config.config import CHROMA_DB_CONFIG

def connect_to_chromadb():
    """
    Establishes a connection to ChromaDB hosted on an EC2 machine using environment-configured parameters.

    Returns:
        chroma_client (chromadb.HttpClient): The ChromaDB client instance.
    """
    # Load environment variables
    load_dotenv()

    # Fetch configuration from CHROMA_DB_CONFIG
    chroma_host = CHROMA_DB_CONFIG.get("CHROMA_HOST")
    chroma_port = CHROMA_DB_CONFIG.get("CHROMA_PORT")
    chroma_project_name = CHROMA_DB_CONFIG.get("CHROMA_PROJECT_NAME")

    if not chroma_host or not chroma_port or not chroma_project_name:
        raise ValueError("Missing ChromaDB configuration parameters. Please check CHROMA_DB_CONFIG.")

    try:
        # Initialize ChromaDB Client
        chroma_client = chromadb.HttpClient(host=chroma_host, port=int(chroma_port))
        print(f"Successfully connected to ChromaDB at {chroma_host}:{chroma_port}")
        print(f"Your ChromaDB project name is: {chroma_project_name}")
        return chroma_client
    except Exception as e:
        print(f"Failed to connect to ChromaDB: {e}")
        return None
