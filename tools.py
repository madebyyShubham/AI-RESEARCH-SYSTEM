from langchain.tools import tool
import requests 
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

tavily= TavilyClient(os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str)->str:
    """ Search the web using Tavily  fro recent and relaible information on a topic. Returns Titles, URLs and snippets."""
    results=tavily.search(query=query, max_results=5)
    print(results)

    out=[]
    for r in results["results"]:
        out.append(
            f"Tittle: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n----\n".join(out)


#print(web_search.invoke("Tell me news about independence day "))

@tool
def scrape_url(url:str)->str:
    """Scrape and return text content from a given url for deeper reading"""

    try:
        response = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Could not Scrape the URL: {str(e)}"


print(scrape_url.invoke("https://www.news18.com/cricket/important-to-be-match-fit-than-gym-fit-gavaskar-calls-out-finger-pointing-over-injuries-ws-l-10276229.html"))

    

