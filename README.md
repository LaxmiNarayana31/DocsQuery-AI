# DocsQuery AI

DocsQuery AI is an intelligent document assistant that enables users to upload PDFs and ask questions about their content. It leverages the power of Google Gemini API for efficient document processing and response generation.

## How It Works

The application follows these steps to provide responses to your questions:

1. **PDF Loading**: The app reads multiple PDF documents and extracts their text content.
2. **Text Chunking**: The extracted text is divided into smaller chunks that can be processed effectively.
3. **Language Model**: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.
4. **Similarity Matching**: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.
5. **Response Generation**: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

## Project Setup

- Clone the repository:
  ```bash
  git clone https://github.com/LaxmiNarayana31/DocsQuery-AI.git
  ```
- Create a virtual environment using pipenv. If you don't have pipenv installed, you can install it by running `pip install pipenv` in your terminal.
  ```bash
  pipenv shell # Create a virtual environment
  pipenv install # Install dependencies
  ```
- Run the application:
  ```bash
  pipenv run main
  ```
  or
  ```bash
  streamlit run main.py
  ```
