from langgraph.graph import StateGraph
from app.agents import retrieve_papers, summarize_paper, compile_insights, evaluate_summary_quality

TrendState = dict

workflow = StateGraph(TrendState)

workflow.add_node("retriever", retrieve_papers)
workflow.add_node("summarizer", summarize_paper)
workflow.add_node("evaluator", evaluate_summary_quality)
workflow.add_node("compiler", compile_insights)

workflow.set_entry_point("retriever")
workflow.add_edge("retriever", "summarizer")
workflow.add_edge("summarizer", "evaluator")

workflow.add_conditional_edges("evaluator", {
    "pass": compile_insights,
    "retry": summarize_paper
})

workflow.set_finish_point("compiler")
graph_executor = workflow.compile()
