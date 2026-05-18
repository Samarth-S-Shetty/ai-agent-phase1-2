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
    """searches theweb forthe information based on the prompt given by the user"""
    tavily_cleint=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result=tavily_cleint.search(query)
    return result
@tool
def write_file(filename:str,content:str)->str:
    """writes content to a.txt file"""
    with open(f"{filename}", "w") as f:
            f.write(content)
            
    return "file written successfully"
    
    

model=ChatOpenAI(model="gpt-4o").bind_tools([web_search,write_file])
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
        elif tool_call["name"]=="write_file":
            result = write_file.invoke(tool_call["args"])
            results.append(ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            ))
            
            
            
    return {"messages": results}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_call"
    return END


graph=StateGraph(AgentState)    
graph.add_node("model_call",call_model)
graph.add_node("tool_call",call_tools)


graph.set_entry_point("model_call")

graph.add_edge("tool_call","model_call")
graph.add_conditional_edges("model_call",should_continue)
app=graph.compile(
    checkpointer=memory,
    interrupt_before=["tool_call"]
    )


config= {"configurable": {"thread_id": "session_2"}}


result=app.invoke({
    "messages":[HumanMessage(content="Research LangGraph and how it differs from LangChain.Then save a detailed summary to a file called langraph_summary")]
    
},config=config)

print("\n--- Agent paused. It wants to call these tools ---")
last=result['messages'][-1]
for tool_call in last.tool_calls:
    print(f"Tool: {tool_call['name']} | Query: {tool_call['args']}")
    
    
while True:
    result = app.invoke(None, config=config)
    last = result["messages"][-1]
    
    if not hasattr(last, "tool_calls") or not last.tool_calls:
        print("\n--- Final Answer ---")
        print(last.content)
        break
    
    print("\n--- Agent wants to call ---")
    for tc in last.tool_calls:
        print(f"Tool: {tc['name']} | Args: {tc['args']}")
    
    approval = input("Approve? (y/n): ")
    if approval != "y":
        print("Stopped.")
        break