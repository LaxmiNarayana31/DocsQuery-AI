from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.helper.llm_helper import GoogleGeminiEmbeddings, GoogleGeminiLLM
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain 
from app.utils.exception_handler import handle_exception


class AIHelper:
    temporary_vectorstore = {}

    # Build a vectorstore from uploaded PDFs
    def build_vectorstore_from_pdfs(pdf_docs):
        try:
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
                        length_function=len
                    )
                    chunks = text_splitter.split_text(text)

                    pdf_name = pdf.name

                    for chunk in chunks:
                        document = Document(
                            page_content = chunk,
                            metadata = {"source": pdf_name}
                        )
                        documents.append(document)
                    

            # Embed the documents
            text_embeddings = GoogleGeminiEmbeddings()
            if text_embeddings is None: return "Error: Could not create embeddings."

            vectorstore = FAISS.from_documents(documents, embedding = text_embeddings)
            AIHelper.temporary_vectorstore = {'vectorstore': vectorstore}
            return AIHelper.temporary_vectorstore['vectorstore']
        except Exception as e:
            return handle_exception(e)


    # Create a conversation chain 
    def initialize_conversation_chain(vectorstore): 
        try: 
            if vectorstore is None: 
                return None 

            google_gemini_llm = GoogleGeminiLLM() 

            retriever = (vectorstore.as_retriever() if hasattr(vectorstore, "as_retriever") else None) 
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
            combine_docs_chain = create_stuff_documents_chain(llm = google_gemini_llm, prompt = prompt) 
            retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain) 
            return retrieval_chain 
        except Exception as e: 
            return handle_exception(e)
    

    def getBotResponse(user_query):
        try:
            vectorstore = AIHelper.temporary_vectorstore.get('vectorstore', None)
            if vectorstore is None:
                return "Vectorstore is not available. Please upload a document first."

            conversation_chain = AIHelper.initialize_conversation_chain(vectorstore)
            if isinstance(conversation_chain, str):  
                return conversation_chain

            response = conversation_chain.invoke({"input": user_query})
            bot_response = response.get('answer', 'No response generated.')  
            return bot_response
        except Exception as e:
            return handle_exception(e)