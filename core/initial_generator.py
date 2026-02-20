from langchain_core.messages import SystemMessage, HumanMessage
from pathlib import Path
from design.design_loader import format_tokens_for_prompt
from core.base_llm import get_llm


class InitialGenerationAgent:
    def __init__(self):
        self.llm = get_llm()
        self.system_prompt = self._load_prompt("system_prompt.txt")
        self.generator_prompt = self._load_prompt("generator_prompt.txt")

    def _load_prompt(self, filename: str) -> str:
        path = Path(__file__).parent.parent / "prompts" / filename
        return path.read_text(encoding="utf-8")

    def generate(self, user_prompt: str) -> str:
        design_rules = format_tokens_for_prompt()

        # SAFE replacement instead of .format()
        final_prompt = (
            self.generator_prompt
            .replace("{design_rules}", design_rules)
            .replace("{user_prompt}", user_prompt)
        )

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=final_prompt)
        ]

        response = self.llm.invoke(messages)

        # Gemini sometimes returns objects, ensure clean string
        if hasattr(response, "content"):
            return response.content.strip()

        return str(response).strip()


# Safe testing block
if __name__ == "__main__":
    agent = InitialGenerationAgent()
    result = agent.generate("A login card with a glassmorphism effect")
    print(result)