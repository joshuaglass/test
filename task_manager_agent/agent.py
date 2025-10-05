# Main Python file for the LiveKit agent
import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import openai
from task_manager import TaskManager

load_dotenv()

CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY")

# Initialize the Cerebras LLM via the OpenAI plugin
llm = openai.LLM.with_cerebras(
    model="llama-3.1-8b-instruct",  # A known Cerebras model
    api_key=CEREBRAS_API_KEY,
)

# Instantiate the Task Manager
task_manager = TaskManager()


async def entrypoint(job: JobContext):
    """
    This is the entrypoint for the agent.
    It's called when a new job is received.
    """
    print("Agent session started")
    session = AgentSession(
        llm=llm,
        tools=[
            task_manager.add_task,
            task_manager.list_tasks,
            task_manager.clear_tasks,
        ],
    )

    # This agent is text-only, so we disable audio input/output
    session.input.audio_source_type = "none"
    session.output.audio_sink_type = "none"

    # Handle incoming text messages from the web client
    @job.room.on("data_received")
    def on_data_received(data: bytes, participant, **kwargs):
        text = data.decode("utf-8")
        print(f"Received text: {text}")
        # Generate a reply and send it back to the user
        session.generate_reply(user_input=text)

    # Send text back to the user
    async for text in session.llm_answers():
        print(f"Sending text: {text}")
        await job.room.local_participant.publish_data(text)

    print("Agent session finished")


async def main():
    """
    Main function to run the agent worker.
    """
    if not CEREBRAS_API_KEY:
        print("CEREBRAS_API_KEY not found in environment variables.")
        print("Please create a .env file and add CEREBRAS_API_KEY=<your-key>")
        exit(1)

    print("Starting agent worker...")
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


if __name__ == "__main__":
    asyncio.run(main())