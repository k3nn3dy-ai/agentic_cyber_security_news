from langchain_community.utilities import GoogleSerperAPIWrapper
from crewai_tools import BaseTool
from pydantic import Field, PrivateAttr
import os
from typing import List

class GoogleNewsSearch(BaseTool):
    """Tool for searching Google News for cybersecurity updates."""
    
    name: str = "Google News Search"
    description: str = "Search for cybersecurity news using Google News"
    
    _serper_api_key: str = PrivateAttr()
    _search_engine: GoogleSerperAPIWrapper = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serper_api_key = os.getenv("SERPER_API_KEY")
        self._search_engine = GoogleSerperAPIWrapper()

    def _run(self, date: str) -> List[dict]:
        """
        Search for cybersecurity news for the last 7 days from a specific date.
        
        Args:
            date (str): The date to search from
            
        Returns:
            List[dict]: List of search results
        """
        query = f"cybersecurity news for the last 7 days from {date}"
        return self._search_engine.results(query)

# Example usage:
if __name__ == "__main__":
    news_search = GoogleNewsSearch()
    results = news_search._run("2024-03-20")
    print(results)
