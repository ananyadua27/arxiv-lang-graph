from app.arxiv_tools import fetch_arxiv_papers
from app.graph import graph_executor
print(fetch_arxiv_papers("machine learning"))
print(graph_executor.invoke({"topic": "machine learning"}))

