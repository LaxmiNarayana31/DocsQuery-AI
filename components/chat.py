import streamlit as st
from app.helper.general_helper import typewriter


def handle_userinput(user_question):
    if not st.session_state.get("conversation"):
        st.warning("Please upload and process your documents before asking questions.")
        return

    print("The question asked by the user is:", user_question)

    with st.chat_message("user"):
        st.markdown(user_question)

    # Get the response from the conversation chain
    response = st.session_state.conversation.invoke({"question": user_question})
    bot_response = response["chat_history"][-1].content

    if st.session_state.selected_chat_index is not None:
        selected_chat = st.session_state.chat_histories[
            st.session_state.selected_chat_index
        ]
        selected_chat["messages"].append({"role": "user", "content": user_question})
        selected_chat["messages"].append({"role": "assistant", "content": bot_response})
    else:
        st.session_state.current_chat.append({"role": "user", "content": user_question})
        st.session_state.current_chat.append(
            {"role": "assistant", "content": bot_response}
        )

    with st.chat_message("assistant"):
        typewriter(bot_response, speed=20)


# Function to save the current chat
def save_current_chat(user_question):
    if st.session_state.current_chat:
        title = (
            st.session_state.current_chat[0]["content"]
            if st.session_state.current_chat
            else "Untitled Chat"
        )
        st.session_state.chat_histories.insert(
            0, {"title": title, "messages": st.session_state.current_chat.copy()}
        )
        st.session_state.current_chat = []


# Function to get a preview of the chat
def get_chat_preview(message):
    words = message.split()
    preview = " ".join(words[:7])
    return f"{preview}..." if len(words) > 10 else message
