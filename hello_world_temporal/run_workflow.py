from dotenv import load_dotenv
load_dotenv()
import asyncio

from run_worker import SayHello
from temporalio.client import Client
import os


async def main():
    # Create client connected to server at the given address
    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS"))

    # Execute a workflow
    result = await client.execute_workflow(
        SayHello.run, "Temporal", id="hello-workflow", task_queue="hello-task-queue"
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())