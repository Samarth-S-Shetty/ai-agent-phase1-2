from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv
from tavily import TavilyClient
import os
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

load_dotenv()
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_core.tools import tool
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]


@tool
def web_search(query:str)->str:
    """searches the web for the information"""
    tavily_client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result=tavily_client.search(query)
    return result
    


model=ChatOpenAI(model="gpt-4o").bind_tools([web_search])
print("model ready")
    
def call_model(state:AgentState):
    response=model.invoke(state["messages"])
    return {"messages":[response]}
    def call_tools(state:AgentState):
        last_message = state["messages"][-1]
        results = []
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "web_search":
                result = web_search.invoke(tool_call["args"])
                results.append(ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                ))
        return {"messages": results}

print("nodes ready")
    
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_call"
    return END


graph=StateGraph(AgentState)    
graph.add_node("model_call",call_model)
graph.add_node("tool_call",call_model)


graph.set_entry_point("model_call")

graph.add_edge("tool_call","model_call")
graph.add_conditional_edges("model_call",should_continue)
app=graph.compile(
    checkpointer=memory,
    interrupt_before=["tool_call"]
    )


config= {"configurable": {"thread_id": "session_2"}}


result=app.invoke({
    "messages":[HumanMessage(content="Research LangGraph and how it differs from LangChain")]
    
},config=config)

print("\n--- Agent paused. It wants to call these tools ---")
last=result['messages'][-1]
for tool_call in last.tool_calls:
    print(f"Tool: {tool_call['name']} | Query: {tool_call['args']}")
    
    
approval=input("pls enter whether u want to proceed further y/n?")
if approval=="y"or approval=="yes":
    result2=app.invoke(None,config=config)
    print("\n--- Final Answer ---")
    print(result2["messages"][-1].content)
else:
    print("agent is stopped by the human!!!")