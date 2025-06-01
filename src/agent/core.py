# Core agent

import os
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper

# Load API keys from environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")

search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
search_tool = Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events or the web"
)

llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

def run(query: str) -> str:
    print(agent.run(query))
    while True:
        query = input("Enter a query: ")
        if query == "exit":
            break
        print(agent.run(query))

run("What is the latest AI model launched by OpenAI?")
