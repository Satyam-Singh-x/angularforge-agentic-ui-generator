
import re
from typing import List
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from core.base_llm import get_llm
from pathlib import Path
from design.design_loader import format_tokens_for_prompt, get_allowed_colors

#===============Pydantic Schema For Validator agent===============================================
class ValidationResult(BaseModel):
    approved: bool = Field(..., description="Whether the component is valid")
    reason_for_disapproval: str = Field(default="", description="Summary reason if disapproved")
    error_points: List[str] = Field(default_factory=list, description="List of specific violations")


#==================Validation Class=====================================================================
class HybridValidatorAgent:

    def __init__(self):
        self.llm = get_llm(temperature=0)
        self.validation_prompt = self._load_prompt("validation_prompt.txt")


    def _load_prompt(self, filename):
        path = Path(__file__).parent.parent / "prompts" / filename
        return path.read_text(encoding="utf-8")


    def _rule_based_checks(self, code: str) -> List[str]:
        errors = []

        # Required Angular structure
        if "import { Component } from '@angular/core';" not in code:
            errors.append("Missing Angular Component import.")

        if "@Component" not in code:
            errors.append("Missing @Component decorator.")

        if "export class" not in code:
            errors.append("Missing exported class definition.")

        # Balanced curly brackets
        if code.count("{") != code.count("}"):
            errors.append("Unbalanced curly brackets.")

        # Balanced template tags
        if code.count("<") != code.count(">"):
            errors.append("Unbalanced HTML angle brackets.")

        # Inline styles not allowed
        if "style=" in code:
            errors.append("Inline styles detected (not allowed).")

        # Unauthorized hex colors
        allowed_colors = get_allowed_colors()
        found_hex = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}", code)

        for color in found_hex:
            if color not in allowed_colors:
                errors.append(f"Unauthorized color detected: {color}")

        return errors


    def _llm_validation(self, code: str) -> ValidationResult:
        design_rules = format_tokens_for_prompt()

        final_prompt = (
            self.validation_prompt
            .replace("{design_rules}", design_rules)
            .replace("{generated_code}", code)
        )

        messages = [
            SystemMessage(content="You are a strict Angular validation agent."),
            HumanMessage(content=final_prompt)
        ]

        structured_llm = self.llm.with_structured_output(ValidationResult)

        result = structured_llm.invoke(messages)

        return result

    def validate(self, code: str) -> ValidationResult:
        rule_errors = self._rule_based_checks(code)

        if rule_errors:
            return ValidationResult(
                approved=False,
                reason_for_disapproval="Rule-based validation failed.",
                error_points=rule_errors
            )

        llm_result = self._llm_validation(code)

        return llm_result









