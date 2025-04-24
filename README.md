
### 👩‍💻 Introduction

I’ve built an intelligent dual-agent research system that can automatically gather and summarize information from the web. It’s designed using modular, modern AI frameworks like **LangGraph** and **LangChain**, integrates **Tavily** for real-time web crawling, and uses **Google Gemini** to generate high-quality responses. The final output is served through a clean and simple **Streamlit** interface.
the researchaibot is deployed on streamlits community cloud  and is running .feel free to give it a try.
---

###  Tech Stack & Frameworks

Here’s a breakdown of the tools and technologies used:

| Component          | Tool / Library             | Purpose                                                                 |
|--------------------|----------------------------|-------------------------------------------------------------------------|
| Language Model      | **Google Gemini (gemini-1.5-pro)** | Used for generating the final, coherent drafted response                |
| Web Crawling        | **Tavily API**             | Performs real-time, intelligent web searches to gather data             |
| Workflow Management | **LangGraph**              | Organizes the step-by-step flow between agents                          |
| Language Integration| **LangChain**              | Framework for chaining LLM calls and handling prompts                   |
| UI & Deployment     | **Streamlit**              | Provides a web-based user interface for querying and displaying results |
| Configuration       | **python-dotenv**          | Loads environment variables (like API keys) securely from `.env` file   |
| Language            | **Python**                 | Primary language used for backend logic                                 |

---

###  System Overview

This system follows a dual-agent architecture:

1. **Research Agent** – Uses Tavily to search for and collect relevant data from the internet based on a user query.
2. **Drafting Agent** – Uses the Google Gemini model to analyze the research and generate a natural-language response.

The LangGraph framework coordinates the flow of data between these two agents to create a smooth, automated pipeline.

---

###  Core Implementation Details

####  Research Agent
Uses Tavily’s search endpoint to fetch data and parse relevant content. It stores this content in the system state for the next step.

####  Drafting Agent
Takes all search results and prompts the Gemini model to generate a summarized response in natural, helpful language. I wrapped the Gemini model using LangChain’s `LLM` base class to make it compatible.

#### LangGraph Workflow
LangGraph creates a directed graph where:
- The research agent node feeds into the drafting agent node.
- After drafting, the system terminates and returns the result.

```python
workflow = StateGraph(dict)
workflow.add_node("research", research_agent)
workflow.add_node("drafting", drafting_agent)
workflow.add_edge("research", "drafting")
workflow.add_edge("drafting", END)
```

---

###  User Interface

The front-end is built with **Streamlit**, allowing users to enter a query and view the AI-generated response in real-time. It makes the system accessible to users who may not have a technical background.

---
### Security & Config

All API keys (Tavily and Gemini) are handled via `.env` files and loaded at runtime using `dotenv`. This keeps sensitive data out of the source code and Git history.

---

###  Highlights & Features

- **Modular agents**: Easy to extend or swap components (e.g., replace Gemini with another model).
- **Search + Summarize** workflow: A useful real-world pattern for research tasks or even knowledge base generation.
- **Gemini wrapper**: Enables full LangChain integration for Gemini, which is not yet officially supported.
- **Minimal UI**: A fast, interactive interface to test and demonstrate the system.

---



