import sys
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from google.cloud import datastore
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Manually point the agent to the system packages where datastore lives
sys.path.append("/usr/local/lib/python3.12/dist-packages")

# --- 1. CONFIG & LOGGING ---
load_dotenv()
MODEL_NAME = os.getenv("MODEL", "gemini-2.5-flash")
PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = "genaihackathon"

# Initialize Datastore Client
datastore_client = datastore.Client(project=PROJECT_ID, database=DATABASE_ID)

# --- 2. CUSTOM TOOLS (Database & Logic) ---

def manage_cloud_tasks(tool_context: ToolContext, action: str, title: str = "") -> dict:
    """Manages tasks in the genaihackathon database."""
    kind = "Task"
    try:
        if action == "add":
            key = datastore_client.key(kind)
            entity = datastore.Entity(key=key)
            entity.update({
                "title": title,
                "status": "pending",
                "timestamp": datetime.utcnow().isoformat()
            })
            datastore_client.put(entity)
            return {"status": "success", "message": f"Added task: {title}"}
        
        elif action == "list":
            query = datastore_client.query(kind=kind)
            tasks = [f"[{t.key.id}] {t['title']}" for t in query.fetch()]
            return {"tasks": tasks if tasks else "No tasks found."}
    except Exception as e:
        return {"error": str(e)}

# Wrap Wikipedia as an ADK tool
wikipedia_tool = LangchainTool(tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()))

# --- 3. MULTI-AGENT ARCHITECTURE ---

# Researcher Agent: Handles the thinking and tool usage
research_agent = Agent(
    name="research_agent",
    model=MODEL_NAME,
    description="Researches information and modifies the cloud database.",
    instruction="""
    You are an intelligent coordinator.
    - If the user wants to KNOW something: Use Wikipedia.
    - If the user wants to REMEMBER/DO something: Use 'manage_cloud_tasks' with action='add'.
    - If the user wants to SEE their list: Use 'manage_cloud_tasks' with action='list'.
    Summarize everything into 'research_data'.
    """,
    tools=[manage_cloud_tasks, wikipedia_tool],
    output_key="research_data"
)

# Formatter Agent: Handles the presentation
formatter_agent = Agent(
    name="formatter_agent",
    model=MODEL_NAME,
    description="Formats the final answer for the user.",
    instruction="""
    Take the RESEARCH_DATA and present it clearly to the user. 
    Confirm any database actions and summarize any research findings.
    
    RESEARCH_DATA: {research_data}
    """
)

# The Orchestrator
root_agent = SequentialAgent(
    name="task_system",
    description="Orchestrates research and task management.",
    sub_agents=[research_agent, formatter_agent]
)

# --- 4. CLI TESTER (Optional) ---
if __name__ == "__main__":
    print(f"🚀 Starting Multi-Agent System on Database: {DATABASE_ID}")
    prompt = "Research 'Generative AI' and add a task to 'Read more about GenAI' to my list."
    result = root_agent.run({"input": prompt})
    print(f"Final Output: {result}")