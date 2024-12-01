import streamlit as st
from app.helper.ai_helper import AiHelper
from app.embedding_models.gemini_embeddings import GoogleGeminiEmbeddings
from components.chat import save_current_chat, get_chat_preview


def display_chat_history():
    st.sidebar.header("Chat History")

    for idx, history in enumerate(st.session_state.chat_histories):
        user_message = (
            history["messages"][0]["content"] if history["messages"] else "No messages"
        )
        if (
            user_message
            == "Hello! I'm DocuQuery AI Assistant. Ask me anything about your documents."
        ):
            continue
        chat_preview = get_chat_preview(user_message)
        if st.sidebar.button(chat_preview, key=f"chat_{idx}"):
            st.session_state.selected_chat_index = idx


def sidebar():
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'",
            accept_multiple_files=True,
        )
        # Process the PDF documents
        if st.button("Process"):
            with st.spinner("Processing"):
                embedding_function = GoogleGeminiEmbeddings()

                # Check if there is an existing vectorstore
                if "vectorstore" in st.session_state:
                    # If vectorstore exists, pass it to AiHelper to add new documents
                    st.session_state.vectorstore = AiHelper.get_vectorstore(
                        pdf_docs, embedding_function
                    )
                else:
                    # If no vectorstore exists, create a new one
                    st.session_state.vectorstore = AiHelper.get_vectorstore(
                        pdf_docs, embedding_function
                    )

                st.session_state.conversation = AiHelper.get_conversation_chain(
                    st.session_state.vectorstore
                )
                st.success("Vectorstore created/updated and ready to use.")

        if st.button("+ New Chat"):
            if st.session_state.current_chat:
                save_current_chat(st.session_state.current_chat[0]["content"])
            st.session_state.new_chat = True
            st.session_state.selected_chat_index = None
            st.session_state.current_chat = []

        display_chat_history()
