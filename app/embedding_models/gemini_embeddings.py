import google.generativeai as genai
from langchain.llms.base import LLM
from langchain_core.embeddings import Embeddings


class GoogleGeminiEmbeddings(Embeddings):
    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            try:
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="retrieval_document",
                )
                embeddings.append(result["embedding"])
            except Exception as e:
                print(f"Error embedding document: {e}")
        return embeddings

    def embed_query(self, query):
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query",
            )
            return result["embedding"]
        except Exception as e:
            print(f"Error embedding query: {e}")
            return None


class GoogleGeminiLLM(LLM):
    def _call(self, prompt, stop=None):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(contents=[{"parts": [{"text": prompt}]}])
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response."

    @property
    def _identifying_params(self):
        return {"model_name": "Gemini 1.5 Flash"}

    @property
    def _llm_type(self):
        return "google_gemini"
