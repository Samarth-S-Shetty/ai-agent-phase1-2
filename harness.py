from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient
import json
import os

load_dotenv()
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def web_tool(query:str)->str:
    try:
        result=tavily.search(query)
        return str(result)
    except Exception as e:
        return f"search failed for {str(e)}"

def write_files(filename:str,content:str)->str:
    try:
        with open(filename,"w") as f:
            f.write(content)
        return "file written sucessfully"
    except Exception as e:
        return f"failed to write :{str(e)}"
    
    
    
# tool registry
TOOL_REGIESTRY={
    "search_tool":web_tool,
    "write_tool":write_files

}
        
print("registry ready!!!!!!!")

TOOL_DEFINITIONS=[
    {
        "type":"function",
        "function":{
            "name":"search_tool",
            "description":"search the web for the information needed",
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{"type":"string"}
                },
                "required":["query"]
            }
        }
        
    },
    {"type":"function",
     "function":{
        "name":"write_tool",
        "description":"Write research summary to a file. Use the filename provided by the user and write the full researched content as content.",
        "parameters":{
            "type":"object",
            "properties":{
                "filename":{"type":"string"},
                "content":{"type":"string"},
            },
            "required":["filename","content"]
        }
     }
        
    }
]

print("tool def ready!!!")


def run_agent(user_input:str):
    messages=[{"role":"user","content":user_input}]
    
    print(f"\n[HARNESS] starting agent for ",{user_input})
    
    while True:
        
        response=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_DEFINITIONS
        )
        ai_message=response.choices[0].message
        if ai_message.tool_calls:
            print(f"[HARNESS] llm wants to call {len(ai_message.tool_calls)}  tools")
        else:
            print("llm wants to final the answer")
        if ai_message.tool_calls:
            messages.append(ai_message)
            for tool_call in ai_message.tool_calls:
                tool_name=tool_call.function.name
                tool_input=json.loads(tool_call.function.arguments)
                
                print(f"[HARNESS] calling {tool_name} with {tool_input}")
                
                if tool_name in TOOL_REGIESTRY:
                    result=TOOL_REGIESTRY[tool_name](**tool_input)
                else:
                    return f"unknown tool {tool_name} with {tool_input}"
                
                print(f"[HARNESS] Result: {str(result)[:50]}...")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            return ai_message.content
        
        
output=run_agent("Research MCP server,use cases and save a summary to mcp.txt")
print(f"\n--- Final Answer ---\n{output}")

                