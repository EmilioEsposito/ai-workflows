import os
from browser_use import Agent, Browser, ChatOpenAI
from browser_use import Tools, ActionResult
import dotenv
import asyncio
dotenv.load_dotenv()

tools = Tools()


@tools.action('Ask user for information or assistance')
def ask_for_human_assistance(prompt: str) -> str:
	print(f'\n✋ The AI Agent is requesting assistance: {prompt}')
	print('\t(press [Enter] when ready to continue)')
	human_response = input(' > ')
	
	return ActionResult(output=human_response.strip(), save_in_memory=True)

# Connect to your existing Chrome browser
browser = Browser(
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    user_data_dir='~/Library/Application Support/Google/Chrome',
    profile_directory='Default',
    allowed_domains=['serniacapital.managebuilding.com'],
    headless=False,
)

sensitive_data = {
    "email": os.getenv('BUILDIUM_EMAIL'),
    "password": os.getenv('BUILDIUM_PASSWORD'),
}

login_task = """
Visit https://serniacapital.managebuilding.com/manager/app/banking/bank-account/377228/bank-feed/matches 
and login with the provided sensitive data credentials. 

You will likely reach a MFA/OTP page. Ask user for the OTP. 

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
Search the page for Bank Transactions that have "duquesne" in them, 
and create a "Buildium entry" for each one by following these steps:

Creating a Buildium entry:
1. Hover over "Add new entry"
2. Enter "Duquesne Light" in the "Vendor" field
3. In Allocations table, on first row:
    - Enter "659" in "Property" column,
    - Enter "Property level" in the "Unit" column
4. Click "Save"

"""

transactions_agent = Agent(
    task=transactions_task,
    browser=browser,
    llm=ChatOpenAI(model='gpt-4.1-mini'),
)


    
async def main():
	await login_agent.run()
	await transactions_agent.run()

if __name__ == "__main__":
    asyncio.run(main())