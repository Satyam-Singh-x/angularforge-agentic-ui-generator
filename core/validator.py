import re
from typing import List
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from core.base_llm import get_llm
from pathlib import Path
from design.design_loader import format_tokens_for_prompt, get_allowed_colors


# ===================== Pydantic Schema =====================

class ValidationResult(BaseModel):
    approved: bool = Field(..., description="Whether the component is valid")
    reason_for_disapproval: str = Field(default="", description="Summary reason if disapproved")
    error_points: List[str] = Field(default_factory=list, description="List of specific violations")


# ===================== Hybrid Validator =====================

class HybridValidatorAgent:

    def __init__(self):
        self.llm = get_llm(temperature=0)
        self.validation_prompt = self._load_prompt("validation_prompt.txt")
        self.parser = PydanticOutputParser(pydantic_object=ValidationResult)

    def _load_prompt(self, filename: str) -> str:
        path = Path(__file__).parent.parent / "prompts" / filename
        return path.read_text(encoding="utf-8")

    # ---------------- Rule-Based Checks ----------------

    def _rule_based_checks(self, code: str) -> List[str]:
        errors = []

        # Angular structure checks
        if "import { Component } from '@angular/core';" not in code:
            errors.append("Missing Angular Component import.")

        if "@Component" not in code:
            errors.append("Missing @Component decorator.")

        if "export class" not in code:
            errors.append("Missing exported class definition.")

        # Bracket balancing
        if code.count("{") != code.count("}"):
            errors.append("Unbalanced curly brackets.")

        if code.count("<") != code.count(">"):
            errors.append("Unbalanced HTML angle brackets.")

        # Inline style restriction
        if "style=" in code:
            errors.append("Inline styles detected (not allowed).")

        # Design token enforcement
        allowed_colors = get_allowed_colors()
        found_hex = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}", code)

        for color in found_hex:
            if color not in allowed_colors:
                errors.append(f"Unauthorized color detected: {color}")

        return errors

    # ---------------- LLM Validation ----------------

    def _llm_validation(self, code: str) -> ValidationResult:
        design_rules = format_tokens_for_prompt()

        format_instructions = self.parser.get_format_instructions()

        final_prompt = (
            self.validation_prompt
            .replace("{design_rules}", design_rules)
            .replace("{generated_code}", code)
        )

        full_prompt = f"""
{final_prompt}

IMPORTANT:
You must strictly follow the output format below.

{format_instructions}
"""

        messages = [
            SystemMessage(content="You are a strict Angular validation agent. Return JSON only."),
            HumanMessage(content=full_prompt)
        ]

        response = self.llm.invoke(messages)

        try:
            return self.parser.parse(response.content)
        except Exception:
            # Fail-safe if parsing fails
            return ValidationResult(
                approved=False,
                reason_for_disapproval="Validator LLM returned malformed output.",
                error_points=["Invalid structured response from validation model."]
            )

    # ---------------- Main Entry ----------------

    def validate(self, code: str) -> ValidationResult:
        # First: deterministic rule-based validation
        rule_errors = self._rule_based_checks(code)

        if rule_errors:
            return ValidationResult(
                approved=False,
                reason_for_disapproval="Rule-based validation failed.",
                error_points=rule_errors
            )

        # Second: structured LLM validation
        return self._llm_validation(code)
