import time
import streamlit as st
from app.utils.exception_handler import handle_exception

def typewriter_effect(text: str, speed: int):
    try:
        lines = text.split("\n") 
        container = st.empty()
        full_text = ""

        for line in lines:
            words = line.split() 
            for index in range(len(words) + 1):
                curr_line = " ".join(words[:index])
                container.markdown(full_text + curr_line)  
                time.sleep(1 / speed)
            # Add line break for Markdown
            full_text += curr_line + "  \n" 
    except Exception as e:
        return handle_exception(e)
