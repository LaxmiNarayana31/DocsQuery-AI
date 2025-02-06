import google.generativeai as genai
from langchain.llms.base import LLM
from langchain_core.embeddings import Embeddings


class GoogleGeminiEmbeddings(Embeddings):
    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document",
            )
            embeddings.append(result["embedding"])
        return embeddings

    def embed_query(self, query):
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query",
        )
        return result["embedding"]


# Custom LLM class to get response from Google Gemini
class GoogleGeminiLLM(LLM):
    def _call(self, prompt, stop=None):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt).text
        return response

    @property
    def _identifying_params(self):
        return {"model_name": "Gemini 1.5 Flash"}

    @property
    def _llm_type(self):
        return "gemini"
