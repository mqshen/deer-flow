# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import json
import logging
import os

from langchain_community.tools import BraveSearch, DuckDuckGoSearchResults
from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper, BraveSearchWrapper
from langchain_community.utilities.searx_search import SearxSearchWrapper

# 兼容不同 langchain_community 版本的 SearxSearchResults 导入
from langchain_community.tools.searx_search.tool import SearxSearchResults


from src.config import SearchEngine, SELECTED_SEARCH_ENGINE
from src.tools.tavily_search.tavily_search_results_with_images import (
    TavilySearchResultsWithImages,
)

from src.tools.decorators import create_logged_tool

logger = logging.getLogger(__name__)

# Create logged versions of the search tools
LoggedTavilySearch = create_logged_tool(TavilySearchResultsWithImages)
LoggedDuckDuckGoSearch = create_logged_tool(DuckDuckGoSearchResults)
LoggedBraveSearch = create_logged_tool(BraveSearch)
LoggedArxivSearch = create_logged_tool(ArxivQueryRun)
LoggedSearxSearch = create_logged_tool(SearxSearchResults)



# Get the selected search tool
def get_web_search_tool(max_search_results: int):
    if SELECTED_SEARCH_ENGINE == SearchEngine.TAVILY.value:
        return LoggedTavilySearch(
            name="web_search",
            max_results=max_search_results,
            include_raw_content=True,
            include_images=True,
            include_image_descriptions=True,
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.DUCKDUCKGO.value:
        return LoggedDuckDuckGoSearch(name="web_search", max_results=max_search_results)
    elif SELECTED_SEARCH_ENGINE == SearchEngine.BRAVE_SEARCH.value:
        return LoggedBraveSearch(
            name="web_search",
            search_wrapper=BraveSearchWrapper(
                api_key=os.getenv("BRAVE_SEARCH_API_KEY", ""),
                search_kwargs={"count": max_search_results},
            ),
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.ARXIV.value:
        return LoggedArxivSearch(
            name="web_search",
            api_wrapper=ArxivAPIWrapper(
                top_k_results=max_search_results,
                load_max_docs=max_search_results,
                load_all_available_meta=True,
            ),
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.SEARX.value:
        return LoggedSearxSearch(
            name="web_search",
            wrapper=SearxSearchWrapper(
                searx_host=os.getenv("SEARX_HOST", "http://localhost:2304"),  # 优先读取 .env 中 SEARX_HOST
                unsecure=False,  # 如有 https 可改为 False
                params={"language": "zh"},  # 可根据需要调整
            ),
            max_results=max_search_results
        )
    else:
        raise ValueError(f"Unsupported search engine: {SELECTED_SEARCH_ENGINE}")


if __name__ == "__main__":
    searx_wrapper = SearxSearchWrapper(
        searx_host=os.getenv("SEARX_HOST", "https://wecom.belink.com/search"),  # 优先读取 .env 中 SEARX_HOST
        unsecure=True,  # 如有 https 可改为 False
        params={"language": "zh"},  # 可根据需要调整
    )
    loggerSearxSearch = LoggedSearxSearch(
        name="web_search",
        wrapper=searx_wrapper,
        max_results=3
    )
    results = loggerSearxSearch.run("what is the weather in France ?", engine="qwant")
    print(json.dumps(results, indent=2, ensure_ascii=False))

