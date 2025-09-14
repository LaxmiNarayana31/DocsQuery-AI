import os
import traceback

from dotenv import load_dotenv
from langchain_google_genai import chat_models
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI, ChatGoogleGenerativeAIError
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from google.api_core.exceptions import ResourceExhausted, InvalidArgument, DeadlineExceeded

from app.exceptions.gemini import GeminiException


load_dotenv(verbose=True)
google_api_key = os.getenv("GOOGLE_API_KEY")

class GeminiLLM:
    @staticmethod
    def get_chat_llm_client():
        try:
            llm = ChatGoogleGenerativeAI(
                model = "gemini-2.0-flash", 
                google_api_key = google_api_key, 
                temperature = 0.8, 
                top_p = 0.85, 
                max_retries = 0
            )
            # Override _chat_with_retry to bypass retries
            chat_models._chat_with_retry = lambda generation_method, **kwargs: generation_method(**kwargs)
            return llm
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)
            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
    
class EmbeddingGenerator:
    _model_name = "models/text-embedding-004"
    _output_dim = 768

    @staticmethod
    def _get_embedding_model():
        return GoogleGenerativeAIEmbeddings(
            model=EmbeddingGenerator._model_name,
            google_api_key=google_api_key
        )

    @staticmethod
    def generate_document_embedding(text: str):
        try:
            document_embedding = EmbeddingGenerator._get_embedding_model().embed_documents(
                texts=[text],
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=EmbeddingGenerator._output_dim
            )
            return document_embedding
        except (ResourceExhausted, ChatGoogleGenerativeAIError, InvalidArgument, DeadlineExceeded) as e:
            return GeminiException.handle_gemini_exception(e)
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)
            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        
    @staticmethod
    def generate_query_embedding(text: str):
        try:
            query_embedding = EmbeddingGenerator._get_embedding_model().embed_query(
                text=text,
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=EmbeddingGenerator._output_dim
            )
            return query_embedding
        except (ResourceExhausted, ChatGoogleGenerativeAIError, InvalidArgument, DeadlineExceeded) as e:
            return GeminiException.handle_gemini_exception(e)
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            print(traceback_str)
            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

