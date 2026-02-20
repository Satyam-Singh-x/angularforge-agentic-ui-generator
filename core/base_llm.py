import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm(model_name="gemini-2.5-flash", temperature=0.2):
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

if __name__ == "__main__":
    get_llm()
    print("done")