import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(model_name: str = "gemini-2.5-flash", temperature: float = 0):

    api_key = st.secrets["GOOGLE_API_KEY"]

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )
