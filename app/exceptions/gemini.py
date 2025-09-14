import re

from google.api_core.exceptions import ResourceExhausted, InvalidArgument, DeadlineExceeded
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError


# Custom exception class for Gemini API errors
class GeminiException(Exception):
    # Handle ResourceExhausted exceptions from Gemini
    @staticmethod
    def resource_exhausted(e: ResourceExhausted):
        error_str = str(e)
        
        quota_metric_match = re.search(r'quota_metric: "(.*?)"', error_str)
        quota_value_match = re.search(r'quota_value: (\d+)', error_str)
        model_match = re.search(r'key: "model"\s+value: "(.*?)"', error_str)

        if quota_metric_match and quota_value_match and model_match:
            # quota_metric = quota_metric_match.group(1)
            quota_value = quota_value_match.group(1)
            model_name = model_match.group(1)
            message = f"Quota exceeded for: model: {model_name}, daily_request_limit: {quota_value}"
            return message if message else error_str
    
    # Handle ChatGoogleGenerativeAIError exceptions
    @staticmethod
    def api_key_error(e: ChatGoogleGenerativeAIError):
        # Catch specific Gemini error and extract clean message
        error_str = str(e)
        match = re.search(r'message:\s*"([^"]+)"', error_str)
        return match.group(1) if match else error_str

    # Handle invalid argument error
    @staticmethod
    def invalid_key_error(e: InvalidArgument):
        error_str = str(e)
        if "API key not valid" in error_str:
            message = "API key not valid. Please pass a valid API key."
        return message if message else error_str

    @staticmethod
    def deadline_exceeded(e: DeadlineExceeded):
        error_str = str(e)
        if "Deadline Exceeded" in error_str:
            message = "The request took too long to process. Please try again."
        return message if message else error_str

    # Handle any Gemini-related exception
    @staticmethod
    def handle_gemini_exception(e: Exception):
        if isinstance(e, ResourceExhausted):
            return GeminiException.resource_exhausted(e)
        elif isinstance(e, ChatGoogleGenerativeAIError):
            return GeminiException.api_key_error(e)
        elif isinstance(e, InvalidArgument):
            return GeminiException.invalid_key_error(e)
        elif isinstance(e, DeadlineExceeded):
            return GeminiException.deadline_exceeded(e)
        else:
            return str(e)