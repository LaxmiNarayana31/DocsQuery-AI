import os
from uuid import uuid4
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.documents import Document
from app.embedding_models.gemini_embeddings import GoogleGeminiLLM


class AiHelper:
    @staticmethod
    def get_vectorstore(pdf_docs, embedding_function):
        documents = []
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            if text:
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                chunks = text_splitter.split_text(text)

                pdf_uuid = str(uuid4())
                pdf_name = pdf.name

                for chunk in chunks:
                    document = Document(
                        page_content=chunk,
                        metadata={"source": pdf_name, "pdf_uuid": pdf_uuid},
                    )
                    documents.append(document)

        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        if not documents:
            return None

        # Create a vectorstore in memory
        vectorstore = FAISS.from_documents(documents, embedding_function)
        return vectorstore

    @staticmethod
    def get_conversation_chain(vectorstore):
        if vectorstore is None:
            return None

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, input_key="question"
        )

        google_gemini_llm = GoogleGeminiLLM()

        retriever = (
            vectorstore.as_retriever() if hasattr(vectorstore, "as_retriever") else None
        )
        if not retriever:
            return "Error: Could not create retriever."

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=google_gemini_llm, retriever=retriever, memory=memory
        )
        return conversation_chain

    @staticmethod
    def handle_userinput_without_streamlit(user_question, vectorstore):
        if vectorstore is None:
            return "No vectorstore found. Please upload PDFs first."

        conversation_chain = AiHelper.get_conversation_chain(vectorstore)
        if isinstance(conversation_chain, str):
            return conversation_chain

        input_dict = {"question": user_question}
        response = conversation_chain(input_dict)
        return response.get("answer", "No response generated.")

    @staticmethod
    def list_documents_in_vectorstore(vectorstore):
        if vectorstore is None:
            return "No vectorstore found."

        dummy_query = " "
        documents = vectorstore.similarity_search(dummy_query, k=10)

        documents_list = []
        unique_uuids = set()
        for document in documents:
            metadata = document.metadata
            pdf_uuid = metadata.get("pdf_uuid")
            if pdf_uuid not in unique_uuids:
                unique_uuids.add(pdf_uuid)
                documents_list.append(
                    {"pdf_name": metadata.get("source"), "pdf_uuid": pdf_uuid}
                )
        return documents_list
