import time
import traceback

import streamlit as st


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
        # Get the traceback as a string
        traceback_str = traceback.format_exc()
        print(traceback_str)
        # Get the line number of the exception
        line_no = traceback.extract_tb(e.__traceback__)[-1][1]
        print(f"Exception occurred on line {line_no}")
        return str(e)
