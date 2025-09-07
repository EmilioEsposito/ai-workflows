import os
from browser_use import Agent, Browser, ChatOpenAI
from browser_use import Tools, ActionResult
import dotenv
import asyncio
import httpx
from datetime import datetime, timezone, timedelta
import time

dotenv.load_dotenv()

tools = Tools()


@tools.action('Ask user for information or assistance')
def ask_for_human_assistance(prompt: str) -> str:
    print(f'\n✋ The AI Agent is requesting assistance: {prompt}')
    print('\t(press [Enter] when ready to continue)')
    human_response = input(' > ')

    return ActionResult(output=human_response.strip(), save_in_memory=True)


@tools.action("Get current UTC time")
async def get_current_utc_time() -> str:
    now_utc = datetime.now(timezone.utc)
    return now_utc.isoformat()


@tools.action("Get OTP for login")
async def get_otp_for_login(login_time_utc_str: str) -> str:
    time.sleep(5)  # wait 5 seconds to receive the sms
    if not os.getenv("OPEN_PHONE_API_KEY"):
        raise Exception("OPEN_PHONE_API_KEY is not set")

    alert_robot_phone_id = "PNWvNqsFFy"

    response = httpx.get(
        f"https://api.openphone.com/v1/messages",
        params={
            "phoneNumberId": alert_robot_phone_id,
            "createdAfter": login_time_utc_str,  # "2022-01-01T00:00:00Z"
            "participants": ["+14155691597"],
        },
        headers={"Authorization": os.getenv("OPEN_PHONE_API_KEY")},
    )
    messages = response.json()["data"]
    if len(messages) == 0:
        return "No OTP found, try 1 more time"
    # get the message with most recent createdAt attribute
    most_recent_message = max(messages, key=lambda x: x["createdAt"])
    otp = most_recent_message["text"][-6:]  # last 6 characters
    return otp


# Try default browser first to test basic functionality
browser = Browser(
    allowed_domains=['serniacapital.managebuilding.com'],
    headless=False,
    keep_alive=True,
)

sensitive_data = {
    "email": os.getenv('BUILDIUM_EMAIL'),
    "password": os.getenv('BUILDIUM_PASSWORD'),
}

login_task = """
1. Visit https://serniacapital.managebuilding.com/manager/app/banking/bank-account/377228/bank-feed/matches 
and fill the text fields with the email and password with the provided sensitive data credentials. 
2. Run the tool `get_current_utc_time` to get the current UTC time.
3. Click the "Sign in" button.
4. You will likely reach a MFA/OTP page. Use the tool `get_otp_for_login` to get the OTP. Use the time from step 2 as the login_time_utc parameter.

The task is complete when you are on the page: https://serniacapital.managebuilding.com/manager/app/banking/bank-account/377228/bank-feed/matches

"""

login_agent = Agent(
    task=login_task,
    browser=browser,
    llm=ChatOpenAI(model='gpt-4.1-mini'),
    sensitive_data=sensitive_data,
    tools=tools,
)

transactions_task = """
On the page, look for "Bank Transactions" that have "duquesne" in them (do NOT use the search bar, the bank transactions are already rendered on the page)
and create a "Buildium entry" for each one (if it does not already exist) by following these steps:

Creating a Buildium entry:
1. If "Add new entry" is not visible for that row, it is already processed, so skip to the next eligble row.
2. Hover over "Add new entry" within the row
3. Click "Check" within the same row
4. A model will popup:
    4.1. Type "Duquesne Light" in the "Vendor" field, and press "Enter" key
    4.2. In Allocations table, on first row:
        4.2.1. Type "659" in "Property" column, and press "Enter" key
        3.2.2. Type "Property level" in the "Unit" column, and press "Enter" key
    4.3. Click "Save"

Move on to the next unprocessed row until all rows with "duquesne" in them are processed.

"""

transactions_agent = Agent(
    task=transactions_task,
    browser=browser,
    llm=ChatOpenAI(model='gpt-4o'),
)


async def main():
	await login_agent.run()
	await transactions_agent.run()

if __name__ == "__main__":
    asyncio.run(main())
