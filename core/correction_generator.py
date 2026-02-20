from langchain_core.messages import SystemMessage, HumanMessage
from pathlib import Path
from design.design_loader import format_tokens_for_prompt
from core.base_llm import get_llm


class CorrectionAgent:
    def __init__(self):
        self.llm = get_llm()
        self.system_prompt = self._load_prompt("system_prompt.txt")
        self.correction_prompt = self._load_prompt("correction_prompt.txt")

    def _load_prompt(self, filename: str) -> str:
        path = Path(__file__).parent.parent / "prompts" / filename
        return path.read_text(encoding="utf-8")

    def correct(self, user_prompt: str, previous_code: str, error_logs: str) -> str:
        design_rules = format_tokens_for_prompt()

        # SAFE string replacement instead of .format()
        final_prompt = (
            self.correction_prompt
            .replace("{design_rules}", design_rules)
            .replace("{user_prompt}", user_prompt)
            .replace("{previous_code}", previous_code)
            .replace("{error_logs}", error_logs)
        )

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=final_prompt)
        ]

        response = self.llm.invoke(messages)

        # Gemini safety extraction
        if hasattr(response, "content"):
            return response.content.strip()

        return str(response).strip()


# Optional testing block
if __name__ == "__main__":
    agent = CorrectionAgent()
    test_code = "import { Component } from '@angular/core';"
    result = agent.correct(
        user_prompt="Login card",
        previous_code=test_code,
        error_logs="Missing template block."
    )
    print(result)