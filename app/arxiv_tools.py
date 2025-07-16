import feedparser
import urllib.parse

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_arxiv_papers(topic: str, max_results: int = 5):
    query = f"all:{topic}"
    encoded_query = urllib.parse.quote(query)  # URL-encode the query to handle spaces and special chars
    url = f"{ARXIV_API_URL}?search_query={encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    feed = feedparser.parse(url)
    
    papers = []
    for entry in feed.entries:
        paper_url = entry.get("id", "")  
        paper = {
            "title": entry.title.strip() if hasattr(entry, 'title') else "No title",
            "summary": entry.summary.strip() if hasattr(entry, 'summary') else "No summary",
            "url": paper_url,
        }
        papers.append(paper)
    return papers
