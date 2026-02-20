import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

load_dotenv()


def get_llm(model_name="gemini-2.5-flash", temperature=0.2):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )

if __name__ == "__main__":
    get_llm()
    print("done")
