import streamlit as st
from langchain_groq import ChatGroq


def get_llm(model_name: str = "llama3-8b-8192", temperature: float = 0):

    if "GROQ_API_KEY" not in st.secrets:
        raise ValueError("GROQ_API_KEY missing in Streamlit secrets.")

    api_key = st.secrets["GROQ_API_KEY"]

    if not api_key:
        raise ValueError("GROQ_API_KEY is empty.")

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        groq_api_key=api_key
    )
