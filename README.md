# arxiv-lang-graph

## Academic Research Trends in CS/EE/DS: Agentic AI Workflow with LangGraph and FastAPI

---

### Overview

**arxiv-lang-graph** is an AI-driven pipeline designed for the extraction, synthesis, and analysis of academic preprints from arXiv.org. It showcases **agentic AI workflows** through a graph-based engine (**LangGraph**) and enables multi-agent collaboration. The backend API, built with **FastAPI**, delivers high-performance, asynchronous REST endpoints tailored for integration with modern frontend/data pipelines.

This project highlights experience with:

- Creating distributed, agent-driven systems with complex dependency graphs.
- Utilizing transformer-based NLP models for abstractive summarization.
- Implementing session persistence and state management via Redis for multi-turn conversational workflows.
- Designing clean API interfaces with asynchronous Python programming patterns.

---

## Demo

#### Search Interface

Efficiently accepts user queries, performs intelligent retrieval, and supports real-time interaction.

![Search](./search.png)

#### Results Display

Presents structured and actionable information with embedded links for quick exploration.

![Results](./results.png)

---

## Core Features

- **ArXiv Query Module**: Implements domain-specific search with customizable filtering and pagination over the arXiv API using **feedparser**.
- **Multi-Agent Workflow Execution**: Sequential and conditional orchestration of agents via **LangGraph**, allowing for complex reasoning pipelines without rigid (linear) control flows.
- **Abstractive Summarization**: Integrates Hugging Face’s `google/flan-t5-base` transformer model fine-tuned for academic text to generate concise, 3-sentence summaries.
- **Stateful Session Management**: Uses **Redis** as an in-memory data store to maintain user context and session state for iterative queries.
- **Extensible API Endpoints**: Asynchronous RESTful endpoints using **FastAPI** supporting JSON payloads.
- **Configurable LLM Backend**: Switchable between local Hugging Face models and OpenAI GPT APIs via environment configuration to optimize for model capabilities.

---

## Agentic AI & LangGraph Architecture

The system showcases **agentic AI** where autonomous agents communicate and cooperate through execution graphs:

- **LangGraph** functions as a declarative workflow engine where agents are nodes and edges represent data/control dependencies.
- Enables **non-linear execution paths** with **conditional branching** and **retry loops**, allowing iterative refinement without hardcoding control logic.

### Workflow & Retry Structure

The multi-agent pipeline is orchestrated through LangGraph with the following logic:

- The **Retriever Agent** fetches relevant papers from arXiv based on the input topic.
- The **Summarizer Agent** generates abstractive summaries for each paper and tracks a retry counter in the state.
- The **Evaluator Agent** assesses the quality of the summaries, checking for criteria such as minimum sentence count and word length.
- If summaries **fail quality criteria** and retry count is below the threshold (5 attempts), LangGraph **routes the workflow back to the Summarizer Agent to retry summarization**, implementing a **non-linear retry loop**.
- If summaries pass quality checks or the retry limit is reached, the workflow continues to the **Compiler Agent**, which aggregates summaries into a cohesive markdown report.

This conditional routing is configured in LangGraph as:

```bash
workflow.add_conditional_edges("evaluator", {
"retry": "summarizer",
"pass": "compiler"
})
```

Each agent function returns a state dictionary including a `"route"` key to signal the next path:

```bash
return {**state, "route": "retry"} # or "pass"
```

---

### Agents Overview

| Agent            | Responsibility                                      | Technology/Technique                                  |
|------------------|----------------------------------------------------|-----------------------------------------------------|
| Retriever Agent  | Query arXiv API, fetch and rank relevant papers    | Feedparser, async HTTP requests                      |
| Summarizer Agent | Generate abstractive summaries for each paper      | Hugging Face Transformers (`flan-t5-base`)          |
| Evaluator Agent  | Evaluate summary quality, decide retry or pass     | Custom Python logic based on summary metrics         |
| Compiler Agent   | Aggregate summaries into formatted markdown report | Python string templating, markdown generation        |

---

## Technical Stack

| Layer                  | Tools / Frameworks                                   |
|------------------------|-----------------------------------------------------|
| Programming Language   | Python 3.9+                                         |
| Workflow Orchestration | LangGraph (graph-based agent execution)             |
| NLP Model Orchestration| LangChain + Hugging Face Transformers (`flan-t5-base`) |
| Web Framework         | FastAPI (async, high throughput REST API)           |
| State Management      | Redis (in-memory data store for session persistence)|
| External APIs         | arXiv via Feedparser                                 |
| Deployment            | uvicorn ASGI server                                  |

---

## Setup & Installation

- Clone repository:  
  `git clone https://github.com/ananyadua27/arxiv-lang-graph.git`  
  `cd arxiv-lang-graph`

- Setup virtual environment and activate:  
  `python -m venv venv`  
  `source venv/bin/activate`

- Install dependencies:  
  `pip install -r requirements.txt`

- Create a `.env` file to configure the Redis URL.

- Run Redis locally (follow Redis official docs).

- Start the FastAPI app:  
  `uvicorn main:app --reload`

---

### Extensibility & Customization

- **Model Backend Switching**: Abstracted LLM interface allows different plug-in transformer models or OpenAI GPT engines with minimal code changes.
- **Workflow Expansion**: LangGraph workflows can be extended to add additional agents for trend forecasting, or multi-modal data analysis.

---

## Notes

- The project prioritizes **local inference** using Hugging Face models to avoid API rate limits and reduce costs but can be adapted to OpenAI’s API by updating configuration.

---

## License

MIT License © Ananya Dua

