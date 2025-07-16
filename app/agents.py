from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from app.arxiv_tools import fetch_arxiv_papers
import re

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base",
    max_length=1024,
    num_beams=7,
    device=-1
)

llm = HuggingFacePipeline(pipeline=generator)

def retrieve_papers(state):
    topic = state.get("topic", "")
    papers = fetch_arxiv_papers(topic, max_results=5)  # limit to 5 papers
    print("[retrieve_papers] Topic:", topic)
    print("[retrieve_papers] Retrieved:", len(papers), "papers")
    print("[retrieve_papers] Paper titles:")
    for i, paper in enumerate(papers, 1):
        print(f"  {i}. {paper['title']}")
    return {**state, "papers": papers}

def summarize_paper(state):
    # increment retry count on each summarization attempt
    retry_count = state.get("retry_count", 0) + 1
    state["retry_count"] = retry_count
    print(f"[summarize_paper] Retry count: {retry_count}")

    papers = state.get("papers", [])
    print("[summarize_paper] Received", len(papers), "papers")

    summaries = []
    for paper in papers:
        prompt = (
            f"Summarize the following research abstract in exactly 3 THIRD-PERSON sentences without repetition. "
            f"Underscore the novelty of the work and its contribution to the field. "
            f"Abstract: {paper['summary']}\n"
            f"Summary ends here."
        )
        try:
            output = llm.invoke(prompt)
            if isinstance(output, list):
                output = output[0]["generated_text"]

            cleaned_output = output.strip()
            summaries.append({
                "title": paper["title"],
                "summary": cleaned_output,
                "url": paper.get("url", "")
            })
            print(f"[summarize_paper] Summary for '{paper['title']}': {cleaned_output}")
        except Exception as e:
            print("[summarize_paper] LLM error:", e)
            summaries.append({
                "title": paper["title"],
                "summary": paper["summary"],
                "url": paper.get("url", "")
            })

    return {**state, "summaries": summaries}

def compile_insights(state):
    summaries = state.get("summaries", [])
    if not summaries:
        report = "No summaries found. Try a different topic."
    else:
        report_lines = []
        for i, s in enumerate(summaries, 1):
            title = s.get("title", "No title")
            summary = s.get("summary", "No summary")
            url = s.get("url", "")
            title_line = f"{i}. [{title}]({url})" if url else f"{i}. {title}"
            report_lines.append(f"{title_line}\n\n{summary}\n")

        report = "\n".join(report_lines)

    print("[compile_insights] Final report:", report)
    return {**state, "report": report}

def evaluate_summary_quality(state):
    summaries = state.get("summaries", [])
    retry_count = state.get("retry_count", 0)
    print(f"[evaluate_summary_quality] Retry count: {retry_count}")

    needs_retry = False
    for s in summaries:
        text = s.get("summary", "")
        num_sentences = text.count('.')
        num_words = len(text.split())
        if num_sentences < 2 or num_words < 35:
            needs_retry = True
            break

    if needs_retry and retry_count < 5:
        print("[evaluate_summary_quality] Summary failed quality check. Retrying...")
        state["route"] = "retry"
    else:
        state["route"] = "pass"
    return state
