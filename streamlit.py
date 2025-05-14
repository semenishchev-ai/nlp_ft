# Usage: streamlit run streamlit.py 
import streamlit as st

def generate_response(s):
    return "A" * ((len(st.session_state.messages) + 1) // 2)

st.title("Local LLM Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    print(st.session_state.messages)
