import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_groq import ChatGroq

from tools import email_tool, llm_tool, validator_tool, ui_tool

# Load .env file
load_dotenv()

# LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# Tool List
tools = [email_tool, llm_tool, validator_tool, ui_tool]

# ReAct Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run Agent
response = agent.run(
    "Fetch the latest financial email, extract structured transaction details, validate them, and push them to frontend."
)

print("\nFINAL OUTPUT:\n")
print(response)