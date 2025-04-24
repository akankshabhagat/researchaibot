import os
from typing import Dict

import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from langchain.llms.base import LLM
from langchain.schema import Generation, LLMResult


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-pro')


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class GeminiLangChainWrapper(LLM):
    def _call(self, prompt: str, stop=None) -> str:
        response = gemini_model.generate_content(prompt)
        return response.text

    @property
    def _llm_type(self) -> str:
        return "google-gemini"

llm = GeminiLangChainWrapper()


def research_agent(state: Dict):
    response = tavily.search(state["query"])
    return {
        "research_results": response.get('results', []),
        "drafted_answer": state["drafted_answer"],
        "query": state["query"]
    }

def drafting_agent(state: Dict):
    context = "\n".join([res.get('content', '') for res in state["research_results"]])
    prompt = f"""
    You are an expert research assistant.
    Based on the search results below, write a clear, concise, and informative summary and points that could help.

    Search Results:
    {context}
    """
    response_text = llm._call(prompt)  
    return {
        "research_results": state["research_results"],
        "drafted_answer": response_text,
        "query": state["query"]
    }


def build_workflow():
    workflow = StateGraph(dict)
    workflow.add_node("research", research_agent)
    workflow.add_node("drafting", drafting_agent)
    workflow.add_edge("research", "drafting")
    workflow.add_edge("drafting", END)
    workflow.set_entry_point("research")
    return workflow.compile()

def run_research_system(query: str) -> str:
    wf = build_workflow()
    result = wf.invoke({
        "research_results": [],
        "drafted_answer": "",
        "query": query
    })
    return result["drafted_answer"]


st.set_page_config(page_title="AI Research Workflow", layout="wide")
st.title("🔬 AI-Powered Research Workflow")

query = st.text_input("Enter your research query:", "")
run = st.button("Run Research")

if run:
    if not query.strip():
        st.warning("Please enter a query before running.")
    else:
        with st.spinner("Running research…"):
            answer = run_research_system(query)
        st.subheader("📝 Drafted Answer")
        st.write(answer)
