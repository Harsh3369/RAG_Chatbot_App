from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load config parameters
from config.config import GPT4O_MINI_CONFIG

#use below embedding if openai key not avilable
# DEVICE = 'cpu'
# embedding_model = HuggingFaceEmbeddings(
#     model_name="BAAI/bge-small-en-v1.5",
#     model_kwargs={"device": DEVICE},
#     encode_kwargs={"normalize_embeddings": True}
# )

embedding_model = OpenAIEmbeddings(openai_api_key=GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI'], model= "text-embedding-3-small")

class DocumentProcessor:
    """
    A class to process documents by chunking them, generating embeddings using OpenAI, 
    and storing the embeddings in ChromaDB.

    Attributes:
        documents (List[Document]): List of document objects to process.
        persist_directory (str): Directory to store ChromaDB data.
    """

    def __init__(self, documents, persist_directory='chroma_data'):
        """
        Initializes the DocumentProcessor class.

        Args:
            documents (List[Document]): List of document objects to process.
            persist_directory (str): Directory to store ChromaDB data.cle
        """
        if not documents:
            raise ValueError("No documents provided for processing.")

        self.documents = documents
        self.persist_directory = persist_directory
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=40)
        self.embeddings = OpenAIEmbeddings(openai_api_key=GPT4O_MINI_CONFIG['OPENAI_API_KEY_4o_MINI'], model= "text-embedding-3-small")
        # self.embeddings = embedding_model

    def chunk_documents(self):
        """Splits the documents into smaller chunks."""
        return self.splitter.split_documents(self.documents)
    

    def store_in_chromadb(self):
        """
        Chunks the documents, embeds them using OpenAI, and stores the vectors in ChromaDB.

        Returns:
            vector_db (Chroma): Chroma vector store instance.
        """
        chunks = self.chunk_documents()
        vector_db = Chroma.from_documents(chunks, self.embeddings, persist_directory=self.persist_directory)
        # vector_db = Chroma.from_documents(chunks, embedding_model, persist_directory=self.persist_directory)

        print(f"Successfully stored {len(chunks)} chunks in ChromaDB.")

        return vector_db

