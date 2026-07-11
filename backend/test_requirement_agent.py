from app.agents.requirement_agent import RequirementAgent


agent = RequirementAgent()


result = agent.execute(
    "Design a 16-bit ALU supporting addition and subtraction"
)


print(result.model_dump())