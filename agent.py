from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient
import json
import os

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "search information on the web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"write_files",
            "description":"gathers the info collected and write it in a files of format .txt",
            "parameters":{
                "type":"object",
                "properties":{
                    "filename":{"type":"string"},
                    "content":{"type":"string"}
                },
                
              "required":["filename","content"] 
            }
            
            
        }
    }
    
]

def run_tool(tool_name, tool_input):
    if tool_name == "web_search":
        result = tavily_client.search(tool_input["query"])
        return str(result)
    elif tool_name =="write_files":
        with open(f"{tool_input['filename']}.txt", "w") as f:
            f.write(tool_input["content"])
        return "file written successfully"

messages = [
    {"role": "user", "content": "Research LangGraph and save a summary to result.txt"}
]

while True:
    response = openai_client.chat.completions.create(
       
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    print(f"\n--- Messages so far: {len(messages)} ---")
    
    ai_message = response.choices[0].message
    print("\n--- AI Response ---")
    print(ai_message)
    
    if ai_message.tool_calls:
        messages.append(ai_message)
        for tool_call in ai_message.tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            print(f"\n--- Tool Called: {tool_name} ---")
            print(f"Input: {tool_input}")
            result = run_tool(tool_name, tool_input)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
    else:
        print("\n--- Final Answer ---")
        print(ai_message.content)
        break