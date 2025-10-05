# LiveKit Task Manager Agent

This project is a simple task manager application powered by a LiveKit agent and the Cerebras LLM. You can interact with the agent through a web interface to add, list, and clear tasks.

## Project Structure

- `task_manager_agent/`: Contains the core application files.
  - `agent.py`: The main LiveKit agent implementation.
  - `task_manager.py`: The task manager tool used by the agent.
  - `generate_token.py`: A script to generate a LiveKit access token for the web client.
  - `requirements.txt`: Python dependencies.
  - `frontend/`: Contains the web interface files.
    - `index.html`: The main HTML file.
    - `style.css`: CSS for styling the interface.
    - `script.js`: JavaScript for connecting to the LiveKit room and handling communication.
- `.env`: Configuration file for API keys and LiveKit URL (you will need to create this).

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create the Environment File

Create a `.env` file in the root of the project and add your API keys and LiveKit URL. You can use the provided `.env.example` as a template.

```
CEREBRAS_API_KEY="<your-cerebras-api-key>"
LIVEKIT_URL="<your-livekit-url>"
LIVEKIT_API_KEY="<your-livekit-api-key>"
LIVEKIT_API_SECRET="<your-livekit-api-secret>"
```

### 3. Install Dependencies

Create a virtual environment and install the required Python packages.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r task_manager_agent/requirements.txt
```

## How to Run

### 1. Start the Agent

Open a terminal, navigate to the `task_manager_agent` directory, and run the agent:

```bash
cd task_manager_agent
python agent.py
```

You should see output indicating that the agent worker is running and waiting for a connection.

### 2. Get a Client Token

The web interface needs a token to connect to the LiveKit room. Open a *second terminal*, navigate to the `task_manager_agent` directory, and run the token generation script:

```bash
cd task_manager_agent
python generate_token.py
```

This will print the LiveKit URL, room name, and a long token string. Copy the token.

### 3. Connect the Web Interface

Open the `task_manager_agent/frontend/index.html` file in your web browser (you can usually just double-click it).

1.  You will see a connection status of "Disconnected".
2.  Paste the token you copied from the previous step into the token input field.
3.  Click the "Connect" button.

The status should change to "Connected", and the chat interface will appear.

### 4. Interact with the Agent

You can now send messages to the agent in the chat box. Try these commands:

- "Add a new task: Buy milk"
- "What are my tasks?"
- "add a task to write a novel"
- "list my tasks"
- "clear all tasks"

The agent will use the Cerebras LLM to understand your requests and manage the task list. The conversation history will be displayed in the chat window.