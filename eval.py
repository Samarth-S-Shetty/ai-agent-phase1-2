GOLDEN_DATASET=[
{
    "question":"what is langgraph?",
    "expected_keywords":["graph", "stateful", "agents", "langgraph"]
},{
     "question":"what is RAG?",
    "expected_keywords":["retrieval", "augmented", "generation", "documents"]
},
{
     "question":"what is vector database?",
    "expected_keywords":["embeddings", "similarity", "search", "vectors"]
}

]

print(f"Golden dataset: {len(GOLDEN_DATASET)} questions")

def evaluator(answer:str,expected_keywords:list)->dict:
    answer_lower=answer.lower()
    
    passed=[]
    failed=[]
    for keywords in expected_keywords:
        if keywords.lower() in answer_lower:
            passed.append(keywords)
        else:
            failed.append(keywords)
    score=len(passed)/len(expected_keywords)
    return {
        "score": score,
        "passed": passed,
        "failed": failed
    }

print("evaluator ready")
import sys
sys.path.append('.')
from harness import run_agent

results = []

for item in GOLDEN_DATASET:
    print(f"\n[EVAL] Testing: {item['question']}")
    
    answer = run_agent(item["question"])
    eval_result = evaluator(answer, item["expected_keywords"])
    
    results.append({
        "question": item["question"],
        "score": eval_result["score"],
        "passed": eval_result["passed"],
        "failed": eval_result["failed"]
    })
    
    print(f"[EVAL] Score: {eval_result['score']:.0%}")
    print(f"[EVAL] Passed keywords: {eval_result['passed']}")
    print(f"[EVAL] Failed keywords: {eval_result['failed']}")

# final score
total = sum(r["score"] for r in results) / len(results)
print(f"\n--- FINAL SCORE: {total:.0%} ---")