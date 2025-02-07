import streamlit as st
from app.streamlit.template.htmlTemplates import css
from app.helper.ai_helper import AIHelper
from app.helper.general_helper import typewriter_effect


def process_user_query(user_question):
    # Check if vectorstore exists in session state
    if "vectorstore" not in st.session_state or st.session_state.vectorstore is None:
        st.warning("Please upload a PDF file first to start the conversation.")
        return

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Generating Response...")

    bot_response = AIHelper.getBotResponse(user_query = user_question)

    with response_placeholder.container():
        typewriter_effect(bot_response, speed=20)

    # Update chat history for selected chat or current chat
    if st.session_state.selected_chat_index is not None:
        # Update the selected chat
        selected_chat = st.session_state.chat_histories[st.session_state.selected_chat_index]
        selected_chat["messages"].append({"role": "user", "content": user_question})
        selected_chat["messages"].append({"role": "assistant", "content": bot_response})
    else:
        # Handle new conversation
        st.session_state.current_chat.append({"role": "user", "content": user_question})
        st.session_state.current_chat.append({"role": "assistant", "content": bot_response})


def store_chat_history():
    """Save the current chat history to the chat histories list with a custom title."""
    if st.session_state.current_chat:
        # Use the first message from the current chat as the title
        title = (st.session_state.current_chat[0]["content"] if st.session_state.current_chat else "Untitled Chat")
        # Insert at the beginning of the list for latest questions first
        st.session_state.chat_histories.insert(0, {"title": title, "messages": st.session_state.current_chat.copy()})
        st.session_state.current_chat = []


def chat_preview(message):
    """Generate a preview of the chat message."""
    words = message.split()
    preview = " ".join(words[:6])
    return f"{preview}..." if len(words) > 10 else message


def display_chat_history():
    st.sidebar.header("Chat History")

    # Display each chat entry as a button in the sidebar
    for idx, history in enumerate(st.session_state.chat_histories):
        user_message = (history["messages"][0]["content"] if history["messages"] else "No messages")
        if (user_message == "Hello! I'm DocuQuery AI Assistant. Ask me anything about your documents."):
            continue
        preview = chat_preview(user_message)
        if st.sidebar.button(preview, key=f"chat_{idx}"):
            st.session_state.selected_chat_index = idx

def main():
    st.set_page_config(page_title="DocsQuery AI", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = []
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = []
    if "selected_chat_index" not in st.session_state:
        st.session_state.selected_chat_index = None
    if "new_chat" not in st.session_state:
        st.session_state.new_chat = False
    # Store vectorstore in session state
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I'm DocuQuery AI Assistant. Ask me anything about your documents.",
            },
        ]

    # Handle PDF upload and processing
    if st.session_state.vectorstore is None:
        with st.sidebar:
            st.subheader("Your documents")
            pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files = True)
            if st.button("Process"):
                with st.spinner("Processing"):
                    vectorstore = AIHelper.build_vectorstore_from_pdfs(pdf_docs)
                    if vectorstore is None:
                        st.warning("Please upload PDF files only.")
                    else:
                        # Store vectorstore in session state
                        st.session_state.vectorstore = vectorstore
                        st.session_state.conversation = AIHelper.initialize_conversation_chain(vectorstore)
                        st.success("PDFs processed successfully.")
    else:
        if st.session_state.conversation is None:
            st.session_state.conversation = AIHelper.initialize_conversation_chain(st.session_state.vectorstore)

        if st.sidebar.button("+ New Chat"):
            if st.session_state.current_chat:
                store_chat_history()
            st.session_state.new_chat = True
            st.session_state.selected_chat_index = None
            st.session_state.current_chat = []

        with st.sidebar:
            display_chat_history()

    _, col2 = st.columns([1, 2.8])
    with col2:
        st.header("DocsQuery AI ! :books:")

    # Display the chat history or current chat
    if (st.session_state.selected_chat_index is None and not st.session_state.current_chat):
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if (message["content"] == "Hello! I'm DocuQuery AI Assistant. Ask me anything about your documents."):
                    typewriter_effect(message["content"], speed=20)
                else:
                    st.markdown(message["content"])

    if st.session_state.selected_chat_index is not None:
        # Display the selected chat's messages
        selected_chat = st.session_state.chat_histories[st.session_state.selected_chat_index]
        for message in selected_chat["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        user_question = st.chat_input(placeholder = "Ask question about your documents")
        if user_question:
            process_user_query(user_question)
    else:
        # Display the current chat's messages
        for message in st.session_state.current_chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        user_question = st.chat_input(placeholder = "Ask question about your documents")
        if user_question:
            process_user_query(user_question)

    if st.session_state.new_chat:
        st.session_state.new_chat = False
