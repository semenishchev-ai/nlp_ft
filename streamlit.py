import streamlit as st
# from transformers import TextStreamer
# from transformers import Gemma3ForConditionalGeneration
# from transformers import AutoProcessor, AutoModelForImageTextToText,AutoModelForCausalLM

import torch
from peft import PeftModel


from llama_cpp import Llama

class Modelka:
    def __init__(self, model_path: str, system_prompt: str, **model_kwargs):
        self.model = Llama(model_path=model_path, **model_kwargs)
        self.system_prompt = system_prompt
        self.context = [{"role": "system", "content": system_prompt}]
    
    def generate(self, message: str, **generation_kwargs) -> str:
        self.context.append({"role": "user", "content": message})
        response = self.model.create_chat_completion(
            messages=self.context,
            stream=False,
            **generation_kwargs
        )
        assistant_message = response['choices'][0]['message']['content']
        self.context.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def reset_context(self) -> None:
        self.context = [{"role": "system", "content": self.system_prompt}]

st.title("Local LLM Chatbot")

modelka = Modelka(model_path="/home/pavel/Downloads/gemma-3-ft(1).gguf",system_prompt="Ты - Лев Толстой. Отвечай пользователю в его стиле.",n_gpu_layers=30,n_ctx=128)


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
        response = modelka.generate(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    print(st.session_state.messages)