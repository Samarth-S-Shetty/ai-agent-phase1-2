# Research Agent

An AI agent that researches any topic from the web and saves a detailed summary to a `.txt` file.

## How it works

1. You give the agent a topic to research
2. LLM decides what queries to search and calls the `web_search` tool
3. Tavily searches the web and returns results
4. LLM enriches and combines all results into a structured summary
5. Agent pauses and asks for your approval before saving
6. On approval, LLM calls `write_file` and saves the summary to a `.txt` file

## Tech Stack

- LangGraph — agent loop and graph structure
- LangChain OpenAI — LLM (gpt-4o)
- Tavily — web search
- MemorySaver — conversation checkpointing

## How to run

```bash
# Create and activate virtual environment
uv venv
.venv\Scripts\activate

# Install dependencies
pip install langgraph langchain-openai tavily-python python-dotenv

# Add your API keys to .env
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key

# Run
python research_agent.py
```

When prompted, type `y` to approve the tool calls and create the `.txt` file.

## Example

```
Input:  "Research LangGraph and how it differs from LangChain. Save summary to langgraph_summary"
Output: langgraph_summary.txt with a detailed structured summary
```