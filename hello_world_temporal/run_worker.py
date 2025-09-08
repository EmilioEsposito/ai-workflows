from dotenv import load_dotenv
load_dotenv()
import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from activities import say_hello
from workflows import SayHello
import os

async def main():
    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS"), namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="hello-task-queue", workflows=[SayHello], activities=[say_hello]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())