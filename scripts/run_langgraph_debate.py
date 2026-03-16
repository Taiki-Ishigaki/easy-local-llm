from orchestrator.langgraph_workflow import run_debate


def main() -> None:
    topic = "複数の LLM を比較しつつ、最終回答を1つにまとめる設計を提案してください。"
    result = run_debate(topic)
    print("Draft:\n")
    print(result.get("draft", ""))
    print("\nCritique:\n")
    print(result.get("critique", ""))
    print("\nFinal:\n")
    print(result.get("final", ""))


if __name__ == "__main__":
    main()
