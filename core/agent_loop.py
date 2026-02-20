from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from core.initial_generator import InitialGenerationAgent
from core.correction_generator import CorrectionAgent
from core.validator import HybridValidatorAgent


# ========================== STATE DEFINITION ==========================

class AgentState(TypedDict):
    user_prompt: str
    current_code: str
    approved: bool
    error_points: List[str]
    attempt_logs: List[Dict[str, Any]]
    retry_count: int
    reason_for_disapproval: str


# ========================== AGENT INSTANCES ==========================

# Initialize once (not per node execution)
generator = InitialGenerationAgent()
validator = HybridValidatorAgent()
corrector = CorrectionAgent()


# ========================== NODE DEFINITIONS ==========================

def generate_node(state: AgentState) -> AgentState:
    """Initial generation node."""
    state["current_code"] = generator.generate(state["user_prompt"])
    return state


def validate_node(state: AgentState) -> AgentState:
    """Hybrid validation node."""
    result = validator.validate(state["current_code"])

    state["approved"] = result.approved
    state["error_points"] = result.error_points
    state["reason_for_disapproval"] = result.reason_for_disapproval

    # Log attempt (attempt numbering starts at 1)
    state["attempt_logs"].append({
        "attempt": state["retry_count"] + 1,
        "code": state["current_code"],
        "approved": result.approved,
        "reason": result.reason_for_disapproval,
        "validation": result.model_dump()  # Pydantic v2
    })

    return state


def correction_node(state: AgentState) -> AgentState:
    """Correction node for rejected outputs."""
    error_text = "\n".join(state["error_points"])

    corrected_code = corrector.correct(
        user_prompt=state["user_prompt"],
        previous_code=state["current_code"],
        error_logs=error_text
    )

    state["current_code"] = corrected_code
    state["retry_count"] += 1

    return state


# ========================== GRAPH BUILDER ==========================

def build_graph(max_retries: int = 2):
    workflow = StateGraph(AgentState)

    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("correct", correction_node)

    workflow.set_entry_point("generate")

    workflow.add_edge("generate", "validate")

    # Conditional retry logic
    def should_correct(state: AgentState):
        if state["approved"]:
            return END

        if state["retry_count"] >= max_retries:
            return END

        return "correct"

    workflow.add_conditional_edges(
        "validate",
        should_correct,
        {
            "correct": "correct",
            END: END
        }
    )

    workflow.add_edge("correct", "validate")

    return workflow.compile()


# ========================== RUN FUNCTION ==========================

def run_agent(user_prompt: str, max_retries: int = 2):
    graph = build_graph(max_retries=max_retries)

    initial_state: AgentState = {
        "user_prompt": user_prompt,
        "current_code": "",
        "approved": False,
        "error_points": [],
        "attempt_logs": [],
        "retry_count": 0,
        "reason_for_disapproval": ""
    }

    final_state = graph.invoke(initial_state)

    return final_state