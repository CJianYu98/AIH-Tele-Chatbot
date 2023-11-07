import os
import pathlib

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from pdf_handler import PDFHandler
from termcolor import colored
from vector_db import VectorDB
from dotenv import load_dotenv

load_dotenv()


class LangChainChatBot:
    def __init__(
        self,
        process_docs: str,
        doc_chunk_size: int = 1000,
        doc_chunk_overlap: int = 150,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.2,
        max_tokens: int = 100,
    ):
        self.process_docs = process_docs

        # For pdf_handler
        self.doc_chunk_size = doc_chunk_size
        self.doc_chunk_overlap = doc_chunk_overlap

        # For LangChain Convo Bot
        self.memory = self._create_buffer_memory()
        self.template = self._create_prompt_template()
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = self._create_model()

        if self.process_docs:
            self._create_pdf_handler(self.doc_chunk_size, self.doc_chunk_overlap)
            self._create_vector_db()
        else:
            self._load_vector_db()
        self.retriever = self.vectordb.vector_db.as_retriever()
        self.qa_chain = self._create_convo_chain()

    def _create_pdf_handler(self, chunk_size: int, chunk_overlap: int) -> None:
        self.pdf_handler = PDFHandler(
            source_docs_dir=os.path.join(os.getenv("PROJECT_DIR"), "docs"),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.doc_splits = self.pdf_handler.get_doc_splits()

    def _create_vector_db(self) -> None:
        self.vectordb = VectorDB(
            db_dir=os.path.join(os.getenv("PROJECT_DIR"), "vectordb"),
            splits=self.doc_splits,
        )

    def _load_vector_db(self) -> None:
        self.vectordb = VectorDB(
            db_dir=os.path.join(os.getenv("PROJECT_DIR"), "vectordb"),
        )

    def _create_buffer_memory(self):
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer",
        )

    def _create_prompt_template(self):
        sys_message = pathlib.Path("./custom_response/system_message.txt").read_text()
        sys_msg_prompt = SystemMessagePromptTemplate.from_template(sys_message)

        template = """Previous conversation: 
        {chat_history}

        Context: 
        {context}

        Question: 
        {question}
        Helpful Answer: """
        human_msg_prompt = HumanMessagePromptTemplate.from_template(template)
        return ChatPromptTemplate.from_messages([sys_msg_prompt, human_msg_prompt])

    def _create_model(self):
        return ChatOpenAI(
            model_name=self.model_name, temperature=self.temperature, request_timeout=120
        )

    def _create_convo_chain(self):
        return ConversationalRetrievalChain.from_llm(
            self.model,
            combine_docs_chain_kwargs={"prompt": self.template},
            retriever=self.retriever,
            return_source_documents=True,
            return_generated_question=True,
            memory=self.memory,
        )

    def _print_msg(self, role: str, message: str):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
        }
        print(colored(f"{role.capitalize()}:\n{message}\n", role_to_color[role]))

    def req_openai(self, user_msg: str) -> str:
        return self.qa_chain({"question": user_msg})["answer"]
        # res = self.qa_chain({"question": user_msg})

        # for i in range(len(res["source_documents"])):
        #     print("\nSource document", i, "\n", res["source_documents"][i])
        
        # return res["answer"]
