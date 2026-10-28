import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9333")
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        print("Page:", page.url)
        
        # Click settings trigger
        btn = page.get_by_role("button", name="Settings trigger")
        if not await btn.is_visible():
            btn = page.locator("button:has-text('Settings trigger'), [aria-label*='Settings trigger'], [data-test-id*='settings']")
        
        print("Clicking settings trigger...")
        await btn.first.click()
        await page.wait_for_timeout(1500)
        
        # Check what popover or dialog opened
        popovers = await page.query_selector_all(".cdk-overlay-container, [role='dialog'], [role='menu'], [role='radiogroup']")
        print(f"Found {len(popovers)} overlay/dialog elements:")
        for pop in popovers:
            txt = await pop.inner_text()
            txt_clean = " | ".join([line.strip() for line in txt.split("\n") if line.strip()])
            print(f"  Overlay text: {txt_clean[:200]}")
            
        # Check radios or buttons inside the overlay
        radios = await page.query_selector_all("[role='radio'], input[type='radio'], button[role='radio'], .mat-radio-button, mat-button-toggle")
        print(f"Found {len(radios)} radio/toggle elements after click:")
        for r in radios:
            name = await r.get_attribute("aria-label") or await r.inner_text()
            print(f"  Item: '{name.strip().replace(chr(10), ' ')}' tag={await r.evaluate('e => e.tagName')}")

asyncio.run(inspect())
