import os
import dotenv
import asyncio
import httpx
from datetime import datetime, timezone
import time
from stagehand import Stagehand, StagehandConfig

dotenv.load_dotenv()


async def get_current_utc_time() -> str:
    """Get current UTC time for OTP timestamp tracking"""
    now_utc = datetime.now(timezone.utc)
    return now_utc.isoformat()


async def get_otp_for_login(login_time_utc_str: str) -> str:
    """Fetch OTP from OpenPhone API for MFA login"""
    time.sleep(5)  # wait 5 seconds to receive the sms
    if not os.getenv("OPEN_PHONE_API_KEY"):
        raise Exception("OPEN_PHONE_API_KEY is not set")

    alert_robot_phone_id = "PNWvNqsFFy"

    response = httpx.get(
        f"https://api.openphone.com/v1/messages",
        params={
            "phoneNumberId": alert_robot_phone_id,
            "createdAfter": login_time_utc_str,
            "participants": ["+14155691597"],
        },
        headers={"Authorization": os.getenv("OPEN_PHONE_API_KEY")},
    )
    messages = response.json()["data"]
    if len(messages) == 0:
        raise Exception("No OTP found, please wait and try again")
    
    # get the message with most recent createdAt attribute
    most_recent_message = max(messages, key=lambda x: x["createdAt"])
    otp = most_recent_message["text"][-6:]  # last 6 characters
    print(f"✅ OTP retrieved: {otp}")
    return otp


async def login_to_buildium(stagehand: Stagehand):
    """Handle Buildium login with MFA"""
    print("🔐 Starting login process...")
    
    target_url = "https://serniacapital.managebuilding.com/manager/app/banking/bank-account/377228/bank-feed/matches"
    
    # Navigate to the page
    await stagehand.page.goto(target_url)
    
    # Fill in credentials
    email = os.getenv('BUILDIUM_EMAIL')
    password = os.getenv('BUILDIUM_PASSWORD')
    
    await stagehand.page.act(f"fill in the email field with {email}")
    await stagehand.page.act(f"fill in the password field with {password}")
    
    # Capture time before clicking sign in (for OTP retrieval)
    login_time = await get_current_utc_time()
    
    await stagehand.page.act("click the sign in button")
    
    # Wait a moment for MFA page to load
    await asyncio.sleep(2)
    
    # Check if we're on MFA page
    current_url = stagehand.page.url
    if "mfa" in current_url.lower() or "verify" in current_url.lower():
        print("📱 MFA required, fetching OTP...")
        otp = await get_otp_for_login(login_time)
        await stagehand.page.act(f"enter the code {otp} in the verification field and submit")
    
    # Wait for navigation to complete
    await stagehand.page.wait_for_url(target_url, timeout=30000)
    print("✅ Login successful!")


async def find_and_process_transaction(stagehand: Stagehand, keyword: str = "duquesne"):
    """Find eligible bank transactions and process them"""
    print(f"🔍 Looking for transactions matching '{keyword}'...")
    
    # Use agent to autonomously handle the complex logic
    agent = stagehand.agent({
        "model": "openai/gpt-4o",
    })
    
    task = f"""
Find and process bank transactions that need matching:

1. Look for table rows with ALL of these conditions:
   - Row header contains "No matching entry:"
   - Bank Transactions column (right side) contains "{keyword}"

2. If you find an eligible row:
   - Hover over "Add new entry" in that row
   - Click "Check" in that same row
   - Wait for the modal to load

3. If no eligible rows exist, report that and stop.

Return whether you found and processed a row.
"""
    
    result = await agent.execute(task)
    print(f"✅ Transaction search complete: {result}")
    return result


async def fill_check_modal(stagehand: Stagehand):
    """Fill out the check entry modal"""
    print("📝 Filling out check entry form...")
    
    # Type and select vendor
    await stagehand.page.act("type 'Duquesne Light' in the Vendor field and press Enter")
    
    # Wait for vendor selection to process
    await asyncio.sleep(1)
    
    # Fill allocations table
    await stagehand.page.act("in the Allocations table first row, type '659' in the Property column and press Enter")
    await asyncio.sleep(0.5)
    await stagehand.page.act("in the Allocations table first row, type 'Property level' in the Unit column and press Enter")
    await asyncio.sleep(0.5)
    
    # Save the entry
    await stagehand.page.act("click the Save button")
    
    print("✅ Check entry saved!")


async def main():
    """Main workflow for processing Buildium bank transactions"""
    
    if not os.getenv("BROWSERBASE_API_KEY"):
        raise Exception("BROWSERBASE_API_KEY environment variable is required")
    
    if not os.getenv("BROWSERBASE_PROJECT_ID"):
        raise Exception("BROWSERBASE_PROJECT_ID environment variable is required")
    
    if not os.getenv("OPENAI_API_KEY"):
        raise Exception("OPENAI_API_KEY environment variable is required")
    
    # Initialize Stagehand with BrowserBase
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=os.getenv("BROWSERBASE_API_KEY"),
        project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
        model_api_key=os.getenv("OPENAI_API_KEY"),
        enable_caching=True,
        verbose=1,
    )
    stagehand = Stagehand(config=config)
    await stagehand.init()
    
    try:
        # Step 1: Login
        await login_to_buildium(stagehand)
        
        # Step 2: Find and process eligible transaction
        found_transaction = await find_and_process_transaction(stagehand, keyword="duquesne")
        
        if found_transaction:
            # Step 3: Fill out the modal
            await fill_check_modal(stagehand)
            print("🎉 Successfully processed Duquesne Light transaction!")
        else:
            print("ℹ️  No eligible transactions found to process")
            
    finally:
        # Close the browser session
        await stagehand.close()
        print("👋 Browser session closed")


if __name__ == "__main__":
    asyncio.run(main())

