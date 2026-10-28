import asyncio
from playwright.async_api import async_playwright

async def dismiss_modal():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9333")
        page = browser.contexts[0].pages[0]
        
        buttons = await page.locator(".cdk-overlay-container button").all()
        print(f"Found {len(buttons)} buttons in modal:")
        for b in buttons:
            name = (await b.inner_text()).strip()
            print(f"  Button: '{name}'")
            if any(k in name.lower() for k in ["agree", "continue", "got it", "ok", "understand", "accept", "confirm"]):
                print(f"  --> Clicking: '{name}'")
                await b.click()
                print("  --> Clicked!")
                
        await page.wait_for_timeout(1000)
        remaining = await page.query_selector_all(".cdk-overlay-backdrop.cdk-overlay-backdrop-showing")
        print(f"Remaining active backdrops: {len(remaining)}")

asyncio.run(dismiss_modal())
