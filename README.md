# lang-graph
# Academic Research Trends in CS/EE/DS: Agentic AI Workflow with LangGraph and FastAPI

This project is an AI-powered system designed to analyze emerging technology trends by automatically retrieving and summarizing recent academic research pre-prints from arXiv.org. It employs agentic reasoning through LangGraph, enabling flexible, multi-step workflows executed by autonomous agents. The system is served via a lightweight FastAPI backend and designed for extensibility and production-ready integration.

## Features

- Retrieves recent arXiv papers based on user-defined research topics
- Summarizes each paper using Hugging Face Transformers (google/flan-t5-base)
- Executes agentic workflows with LangGraph for retrieval, summarization, and report generation
- Maintains session state using Redis for efficient multi-turn interactions
- Provides an API endpoint for triggering full analysis pipelines
- Returns structured, markdown-compatible reports for UI display or downstream applications

## Agentic AI and LangGraph

This project demonstrates the use of agentic AI, where independent agents collaborate through a graph-based execution model. By using LangGraph, the system handles non-linear reasoning tasks such as:
- Sequential data retrieval and summarization
- Adaptive control over workflow transitions
- Clean modular structure that supports future expansion (e.g., trend prediction, citation graphs)

LangGraph enables reliable, scalable workflows without hardcoding logic or sequencing, making it well-suited for research, automation, and intelligent report generation.

## Tech Stack

- Python 3.9+  
- Python 3.9+ – Core programming language
- LangGraph – Graph-based agent workflow engine
- LangChain + Hugging Face Transformers – Large language model orchestration (flan-t5-base)
- FastAPI – High-performance REST API framework
- Redis – Session state storage and persistence
- Feedparser – Interface for querying the arXiv API

## System Architecture

The core pipeline includes:
- Retriever Agent – Queries arXiv and fetches top relevant papers
- Summarizer Agent – Uses a transformer model to generate concise, 3-sentence summaries
- Compiler Agent – Formats output as a numbered, markdown-ready report

The agents are executed in sequence using a LangGraph workflow that allows for future branching or feedback integration. 
A system diagram is included below:

![LangGraph Architecture](./flow.png)

## Setup

1. Clone the repo

   git clone https://github.com/yourusername/lang-graph.git
   cd lang-graph

2. Create/activate a virtual environment

    python -m venv venv
    source venv/bin/activate

3. Install dependencies

    pip install -r requirements.txt

4. Create .env file to configure Redis URL

5. Run Redis locally (follow Redis docs)

5. Start the FastAPI app

    uvicorn main:app --reload

## Note

1. This project uses Hugging Face models for local inference to avoid OpenAI API costs and quota limits.

2. If you want to switch back to OpenAI GPT-4 or GPT-3.5, update the LLM initialization in app/agents.py and add your OpenAI API key in .env.