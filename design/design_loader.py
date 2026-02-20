import json
from pathlib import Path

DESIGN_PATH = Path(__file__).parent / "design-system.json"


def load_design_tokens():
    with open(DESIGN_PATH, "r") as f:
        return json.load(f)


def format_tokens_for_prompt():
    tokens = load_design_tokens()

    formatted = f"""
You must strictly follow this design system:

Allowed Colors:
Primary: {tokens['colors']['primary']}
Secondary: {tokens['colors']['secondary']}
Background: {tokens['colors']['background']}
Text: {tokens['colors']['text']}

Border Radius:
Default: {tokens['borderRadius']['default']}

Font Family:
{tokens['font']['family']}

Do not use any other colors, radius, or fonts.
"""

    return formatted


def get_allowed_colors():
    tokens = load_design_tokens()
    return list(tokens["colors"].values())

