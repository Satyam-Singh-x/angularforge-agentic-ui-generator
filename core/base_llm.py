import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(model_name: str = "gemini-1.5-flash", temperature: float = 0):

    if "GOOGLE_API_KEY" not in st.secrets:
        raise ValueError("GOOGLE_API_KEY missing in Streamlit secrets.")

    api_key = st.secrets["GOOGLE_API_KEY"]

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is empty.")

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )
