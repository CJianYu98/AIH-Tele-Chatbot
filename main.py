from tele_bot import bot as tele_bot

if __name__ == "__main__":
    # # Load PDF documents and split them into chunks
    # pdf_handler = PDFHandler(
    #     source_docs_dir="/Users/chenjianyu/Library/Mobile Documents/com~apple~CloudDocs/SMU/SMU Module Materials/Y5S1/COR2221 AI and Humanity/Project/docs",
    #     chunk_size=1000,
    #     chunk_overlap=150,
    # )
    # doc_splits = pdf_handler.get_doc_splits()

    # # Create a vector database
    # vector_db = VectorDB(
    #     db_dir="/Users/chenjianyu/Library/Mobile Documents/com~apple~CloudDocs/SMU/SMU Module Materials/Y5S1/COR2221 AI and Humanity/Project/vectordb",
    #     splits=doc_splits,
    # )

    # Instantiate a chatbot and run the conversation
    # chatbot = ChatBot(vector_db=vector_db)
    # chatbot = LangChainChatBot()
    # chatbot.run_convo()

    # Start tele bot
    print("TELE BOT STARTED....")
    tele_bot.infinity_polling()
