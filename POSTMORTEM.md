# Post-Mortem: Building a Harness from Scratch vs LangGraph

## What I Built
Built the same AI research agent twice:
- `harness.py` — raw Python, no frameworks, built everything from scratch
- `research_agent.py` — same agent using LangGraph

## What LangGraph Gave Me For Free

| Thing | harness.py | research_agent.py |
|---|---|---|
| Agent loop | wrote `while True` manually | LangGraph handles it |
| Tool routing | wrote `if/elif` manually | `add_conditional_edges` |
| Tool definition | manual JSON schema | `@tool` decorator |
| Memory | manual `messages` list | `MemorySaver` |
| Human in the loop | manual `input()` | `interrupt_before` |
| Logging | manual `print()` | built in |

## What I Learned
LangGraph is just a well-engineered version of harness.py.
Building the raw loop first made everything in LangGraph click instantly.
Understanding what happens under the hood is the difference between
an engineer who can debug production issues and one who can't.
there are many ways to build ai harness

