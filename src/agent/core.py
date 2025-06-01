# Core agent

import os
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper

def create_search_tool() -> Optional[Tool]:
    """Create search tool if SerpAPI key is available."""
    if not settings.serpapi_api_key:
        print("Warning: SERPAPI_API_KEY not found. Search functionality disabled.")
        return None
    
    search = SerpAPIWrapper(serpapi_api_key=settings.serpapi_api_key)
    return Tool(
        name="search",
        func=search.run,
        description="Useful for when you need to answer questions about current events or search the web"
    )

def create_agent() -> AgentExecutor:
    """Create and configure the LangChain agent."""
    
    # Initialize LLM
    llm = ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.model_name,
        temperature=settings.model_temperature,
        max_tokens=settings.model_max_tokens
    )
    
    # Initialize tools
    tools = []
    search_tool = create_search_tool()
    if search_tool:
        tools.append(search_tool)
    
    if not tools:
        print("Warning: No tools available. Agent will have limited functionality.")
    
    # Create prompt template
    prompt = PromptTemplate(
        input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
        template="""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
    )
    
    # Create agent
    if tools:
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=settings.agent_verbose,
            handle_parsing_errors=True,
            max_iterations=3
        )
    else:
        # Fallback: create simple executor without tools
        class SimpleExecutor:
            def invoke(self, inputs):
                question = inputs.get("input", "")
                response = llm.invoke(question)
                return {"output": response.content}
        
        agent_executor = SimpleExecutor()
    
    return agent_executor


def run(query: str) -> str:
    """Run a single query through the agent."""
    if not query.strip():
        return "Please provide a valid query."
    
    try:
        agent = create_agent()
        result = agent.invoke({"input": query})
        return result.get("output", "No response generated.")
    except Exception as e:
        return f"Error: {str(e)}"


def interactive_mode():
    """Run the agent in interactive mode."""
    print("🤖 Agent started! Type 'exit' to quit.")
    agent = create_agent()
    
    while True:
        try:
            query = input("\n🔮 Enter your question: ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                print("Please enter a question.")
                continue
                
            result = agent.invoke({"input": query})
            print(f"\n🤖 Answer: {result.get('output', 'No response generated.')}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


