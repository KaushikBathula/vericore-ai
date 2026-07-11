import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.requirement_agent import RequirementAgent


def main():
    agent = RequirementAgent()

    requirement = (
        "Design a 16-bit ALU supporting "
        "ADD, SUB, AND and OR."
    )

    result = agent.execute(requirement)

    print("\n========== RequirementSpec ==========\n")
    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    main()