from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


class VectorDB:
    def __init__(self, db_dir: str, splits: list = None):
        self.db_dir = db_dir
        self.splits = splits 
        self.vector_db = self._create_db()

    def _create_db(self):
        if self.splits is None:
            return Chroma(persist_directory=self.db_dir, embedding_function=OpenAIEmbeddings())
        return Chroma.from_documents(
            documents=self.splits, embedding=OpenAIEmbeddings(), persist_directory=self.db_dir
        )

    def _concat_docs(self, docs: list):
        docs_combined = [d[0].page_content for d in docs]
        return "\n\n".join(docs_combined)

    def retrieve_sim_docs(self, question: str, topk: int):
        docs = self.vector_db.similarity_search_with_score(question, topk)
        return self._concat_docs(docs)
