import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyMuPDFLoader, 
    UnstructuredWordDocumentLoader, 
    TextLoader
)

# Load environment variables
load_dotenv()

class DocumentLoader:
    """
    A class to load documents using the appropriate loader based on the file extension.
    
    Supported formats:
    - PDF (.pdf) → Uses `PyMuPDFLoader`
    - DOCX (.docx) → Uses `UnstructuredWordDocumentLoader`
    - TXT (.txt) → Uses `TextLoader`
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()
        
    def get_loader(self):
        """
        Determines the appropriate loader based on the file extension.
        
        Returns:
            A document loader instance.
        
        Raises:
            ValueError: If the file type is unsupported.
        """
        if self.extension == '.pdf':
            print(f'Loading PDF document loader for {self.file_path}')
            return PyMuPDFLoader(self.file_path)
        elif self.extension == '.docx':
            print(f'Loading DOCX document loader for {self.file_path}')
            return UnstructuredWordDocumentLoader(self.file_path)
        elif self.extension == '.txt':
            print(f'Loading TXT document loader for {self.file_path}')
            return TextLoader(self.file_path)
        else:
            raise ValueError(f'Unsupported file type {self.extension}')
    
    def load(self):
        """
        Loads the document using the determined loader.
        
        Returns:
            List[Document]: A list of loaded document objects.
        """
        loader = self.get_loader()
        return loader.load()


