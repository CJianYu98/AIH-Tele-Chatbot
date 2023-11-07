from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFHandler:
    def __init__(self, source_docs_dir: str, chunk_size: int, chunk_overlap: int):
        self.docs_dir = source_docs_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _load_docs(self):
        loader = PyPDFDirectoryLoader(self.docs_dir)
        self.pages = loader.load()

    def _split_docs(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, length_function=len
        )
        return text_splitter.split_documents(self.pages)

    def get_doc_splits(self):
        self._load_docs()
        return self._split_docs()
