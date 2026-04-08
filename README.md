TaskMind: Multi-Agent Task Orchestrator
Live Deployment: https://ai-assistant6-178533930066.europe-west1.run.app/

🚀 Overview
TaskMind is a sophisticated Multi-Agent AI System built using the Google Agent Development Kit (ADK) and Gemini 2.5 Flash. It moves beyond simple chat interactions by creating an "Agentic Workflow" that researches real-world information and manages a persistent task database autonomously.

Key Capabilities:
Autonomous Research: Grounded information gathering via Wikipedia API.

Persistent Memory: State-management using Google Cloud Datastore.

Agentic Handoff: Uses a Sequential Agent architecture to separate reasoning from presentation.

🏗️ Architecture
The system utilizes a hierarchical "Manager-Specialist" design:

Orchestrator (SequentialAgent): Manages the logic flow and data passing.

Research Agent: The "Specialist" that determines which tools to call (Wikipedia for facts, Datastore for tasks).

Formatter Agent: The "Presenter" that synthesizes raw tool data into a friendly, conversational response.

🛠️ Technical Stack
LLM: Gemini 2.5 Flash (via Vertex AI)

Framework: Google ADK (Agent Development Kit)

Database: Google Cloud Datastore (NoSQL Mode)

Deployment: Google Cloud Run (Dockerized)

Language: Python 3.12

📖 How to Use
You can interact with the agent using natural language prompts.

Try these examples:

"Search for the history of the Rumi Darwaza and add a task to 'Visit Old Lucknow' to my list."

"What are the latest developments in Generative AI? Save a reminder to 'Read GenAI papers' in my database."

"List all the tasks currently saved in my cloud database."

⚙️ Local Development
To run this project locally:

Clone the repository:

Bash
git clone <your-repo-url>
cd ai_ml_engineer_assistant
Set up Environment Variables:
Create a .env file with:

Plaintext
PROJECT_ID=your-google-cloud-project-id
MODEL=gemini-2.5-flash
Install Dependencies:

Bash
pip install -r requirements.txt
Run the Agent:

Bash
python agent.py
🛡️ Security & Scalability
IAM Roles: The system uses a dedicated Service Account with roles/datastore.user permissions.

Scalability: Built on Cloud Run, the application scales to zero when not in use and handles high-concurrency through asynchronous agent execution.
