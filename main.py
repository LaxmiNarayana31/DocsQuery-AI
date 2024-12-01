import streamlit as st
from dotenv import load_dotenv
from components.chat import handle_userinput
from components.sidebar import sidebar
from template.htmlTemplates import css


def main():
    load_dotenv()
    st.set_page_config(page_title="DocsQuery AI", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

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

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I'm an DocsQuery AI Assistant. Ask me anything about your documents.",
            },
        ]

    sidebar()

    col1, col2 = st.columns([1, 2.8])
    with col2:
        st.header("DocsQuery AI ! :books:")

    if (
        st.session_state.selected_chat_index is None
        and not st.session_state.current_chat
    ):
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if st.session_state.selected_chat_index is not None:
        selected_chat = st.session_state.chat_histories[
            st.session_state.selected_chat_index
        ]
        for message in selected_chat["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        user_question = st.chat_input(placeholder="Ask question about your documents")
        if user_question:
            handle_userinput(user_question)
    else:
        for message in st.session_state.current_chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        user_question = st.chat_input(placeholder="Ask question about your documents")
        if user_question:
            handle_userinput(user_question)

    if st.session_state.new_chat:
        st.session_state.new_chat = False


if __name__ == "__main__":
    main()
