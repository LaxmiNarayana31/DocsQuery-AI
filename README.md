# DocsQuery AI 🚀

**Your intelligent assistant for querying documents.**

DocsQuery AI is a powerful and intuitive application that allows you to have conversations with your documents. Upload your PDFs, and ask questions to get instant, context-aware answers. Powered by Google Gemini, this tool transforms your documents into a searchable knowledge base.

## Key Features ✨

- **Multiple Document Support**: Upload and query multiple PDF documents at once.
- **Intelligent Question Answering**: Leverages state-of-the-art language models (Google Gemini) to understand and answer your questions.
- **Vector-Based Search**: Utilizes FAISS for efficient and accurate similarity search to find the most relevant information in your documents.
- **User-Friendly Interface**: A clean and simple interface built with Streamlit for a seamless user experience.
- **Easy to Set Up**: Get up and running in a few simple steps with Pipenv.

## How It Works 🤖

The application implements a Retrieval-Augmented Generation (RAG) pipeline:

1.  **Document Ingestion**: PDFs are loaded and their text content is extracted.
2.  **Text Chunking**: The extracted text is split into smaller, manageable chunks.
3.  **Vectorization**: Each chunk is converted into a numerical representation (embedding) using Google's language models.
4.  **Indexing**: The embeddings are stored in a FAISS vector store for fast retrieval.
5.  **Query & Retrieval**: When you ask a question, it's also embedded, and the most similar text chunks are retrieved from the vector store.
6.  **Response Generation**: The retrieved chunks and your question are passed to the Gemini model, which generates a human-like answer based on the provided context.

## Technology Stack 🛠️

- **Backend**: Python
- **Frontend**: Streamlit
- **AI/ML**:
  - Google Gemini API
  - LangChain
  - FAISS (for vector storage)
- **Dependency Management**: Pipenv

## Getting Started 🏁

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.12
- Pipenv (`pip install pipenv`)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/LaxmiNarayana31/DocsQuery-AI.git
    cd DocsQuery-AI
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    pipenv shell
    pipenv install
    ```

### Configuration

1.  **Create a `.env` file** in the root of the project by copying the sample file:

    ```bash
    cp .env.sample .env
    ```

2.  **Add your Google API Key** to the `.env` file:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage 🚀

To start the application, run the following command from the root directory:

```bash
pipenv run main
```

This will launch the Streamlit application in your web browser.

Alternatively, you can run:

```bash
streamlit run main.py
```

## Contributing 🤝

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.
