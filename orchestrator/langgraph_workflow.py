from dataclasses import dataclass
from typing import TypedDict

from app.config import DEFAULT_MODEL, load_model_definitions
from app.llm_client import chat


class DebateState(TypedDict, total=False):
    topic: str
    proposer_model: str
    critic_model: str
    judge_model: str
    draft: str
    critique: str
    final: str


@dataclass(frozen=True)
class DebateModels:
    proposer: str
    critic: str
    judge: str


def _default_models() -> DebateModels:
    aliases = [model.model_name for model in load_model_definitions()]
    proposer = aliases[0] if aliases else DEFAULT_MODEL
    critic = aliases[1] if len(aliases) > 1 else proposer
    judge = aliases[2] if len(aliases) > 2 else critic
    return DebateModels(proposer=proposer, critic=critic, judge=judge)


def _propose(state: DebateState) -> DebateState:
    model = state.get("proposer_model", _default_models().proposer)
    draft = chat(
        (
            "You are the proposer. Write a concise first draft that addresses the topic "
            "with a practical recommendation.\n\n"
            f"Topic: {state['topic']}"
        ),
        model=model,
    )
    return {"draft": draft}


def _critique(state: DebateState) -> DebateState:
    model = state.get("critic_model", _default_models().critic)
    critique = chat(
        (
            "You are the critic. Review the draft and list the biggest weaknesses, "
            "risks, and missing considerations.\n\n"
            f"Topic: {state['topic']}\n\nDraft:\n{state['draft']}"
        ),
        model=model,
    )
    return {"critique": critique}


def _judge(state: DebateState) -> DebateState:
    model = state.get("judge_model", _default_models().judge)
    final = chat(
        (
            "You are the judge. Produce the final answer by combining the draft with the "
            "critique. Keep the answer practical and explicit about tradeoffs.\n\n"
            f"Topic: {state['topic']}\n\n"
            f"Draft:\n{state['draft']}\n\n"
            f"Critique:\n{state['critique']}"
        ),
        model=model,
    )
    return {"final": final}


def build_debate_graph():
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "langgraph is not installed. Install with `uv sync --extra orchestration`."
        ) from exc

    graph = StateGraph(DebateState)
    graph.add_node("propose", _propose)
    graph.add_node("critique", _critique)
    graph.add_node("judge", _judge)
    graph.add_edge(START, "propose")
    graph.add_edge("propose", "critique")
    graph.add_edge("critique", "judge")
    graph.add_edge("judge", END)
    return graph.compile()


def run_debate(
    topic: str,
    models: DebateModels | None = None,
) -> DebateState:
    selected = models or _default_models()
    graph = build_debate_graph()
    return graph.invoke(
        {
            "topic": topic,
            "proposer_model": selected.proposer,
            "critic_model": selected.critic,
            "judge_model": selected.judge,
        }
    )
