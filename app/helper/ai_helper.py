import traceback

from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from app.helper.llm_helper import GeminiLLM, EmbeddingGenerator
from app.helper.document_helper import DocumentHelper

class AIHelper:
    """
    Core AI helper for:
    1. Building vectorstores from uploaded documents
    2. Creating a conversation chain
    3. Getting responses from the bot
    """
    temporary_vectorstore = {}

    # ---------------- Build Vectorstore ----------------
    @staticmethod
    def build_vectorstore_from_docs(uploaded_docs):
        """
        uploaded_docs: list of files uploaded by user
        Returns FAISS vectorstore
        """
        try:
            documents = []

            for file in uploaded_docs:
                # Extract text using the new DocumentHelper
                text = DocumentHelper.extractText(file)
                if not text:
                    continue  # skip empty files

                # Split text into chunks
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_text(text)
                file_name = file.name

                for chunk in chunks:
                    doc = Document(
                        page_content=chunk,
                        metadata={"source": file_name}
                    )
                    documents.append(doc)

            if not documents:
                return "No valid text found in uploaded documents."

            # Create embeddings using your helper
            embeddings = EmbeddingGenerator._get_embedding_model()
            if embeddings is None:
                return "Error: Could not create embeddings."

            # Build FAISS vectorstore
            vectorstore = FAISS.from_documents(documents, embedding=embeddings)
            AIHelper.temporary_vectorstore = {'vectorstore': vectorstore}
            return vectorstore
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)
            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    # ---------------- Initialize Conversation Chain ----------------
    @staticmethod
    def initialize_conversation_chain(vectorstore):
        """
        vectorstore: FAISS object
        Returns a retrieval + LLM chain
        """
        try:
            if vectorstore is None:
                return None

            # Get Gemini LLM client
            llm = GeminiLLM.get_chat_llm_client()

            retriever = vectorstore.as_retriever() if hasattr(vectorstore, "as_retriever") else None
            if not retriever:
                return "Error: Could not create retriever."

            prompt_template = """
            1. You are a helpful assistant.
            2. Give a clear and concise answer.
            3. If you don't know the answer, say that you don't know. Don't make up an answer.
            4. If the question is not related to the context, politely respond that you are tuned to the context.
            5. If the question is inappropriate, respond with a neutral answer.

            Context:
            {context}

            Question: {input}

            Helpful Answer:
            """
            prompt = PromptTemplate.from_template(prompt_template)

            combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
            retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
            return retrieval_chain
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)
            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    # ---------------- Get LLM Response ----------------
    @staticmethod
    def get_llm_response(user_query):
        """
        Run user query against the current conversation chain
        """
        try:
            vectorstore = AIHelper.temporary_vectorstore.get('vectorstore', None)

            conversation_chain = AIHelper.initialize_conversation_chain(vectorstore)
            if conversation_chain is None:
                return "Please re-upload the documents."
            if isinstance(conversation_chain, str):
                return conversation_chain

            response = conversation_chain.invoke({"input": user_query})
            llm_response = response.get('answer', 'No response generated.')
            return llm_response
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)
            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        