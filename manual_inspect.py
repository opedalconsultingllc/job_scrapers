#!/usr/bin/env python3
"""
Manual Inspection Helper
Opens browser, performs search, and pauses for manual inspection
"""

import asyncio
from playwright.async_api import async_playwright


async def manual_inspection():
    """Open browser and pause for manual inspection."""
    
    print("\n" + "="*80)
    print("MANUAL INSPECTION MODE")
    print("="*80)
    print("\nThis script will:")
    print("1. Open Chrome browser")
    print("2. Navigate to Microsoft Careers")
    print("3. Fill in the search for 'AI'")
    print("4. Show results page")
    print("5. PAUSE so you can inspect elements\n")
    print("="*80)
    
    async with async_playwright() as p:
        # Launch visible browser
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-notifications',
                '--disable-popup-blocking',
                '--start-maximized'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            permissions=[],
        )
        
        page = await context.new_page()
        
        # Step 1: Navigate
        print("\n📍 Step 1: Navigating to Microsoft Careers...")
        await page.goto("https://careers.microsoft.com/v2/global/en/home.html", 
                       wait_until='networkidle')
        await asyncio.sleep(3)
        print("✅ Homepage loaded")
        
        # Step 2: Fill search
        print("\n🔍 Step 2: Filling search box with 'AI'...")
        try:
            await page.fill('#search-box9', 'AI')
            print("✅ Search box filled")
        except Exception as e:
            print(f"❌ Could not fill search box: {e}")
        
        await asyncio.sleep(2)
        
        # Step 3: Submit search
        print("\n⏎ Step 3: Pressing Enter to search...")
        await page.keyboard.press('Enter')
        await page.wait_for_load_state('networkidle', timeout=30000)
        await asyncio.sleep(5)
        print("✅ Results page loaded")
        
        # Step 4: Show current state
        print("\n" + "="*80)
        print("RESULTS PAGE LOADED - READY FOR INSPECTION")
        print("="*80)
        
        # Get results counter
        try:
            results_h1 = await page.evaluate("() => document.querySelector('h1')?.textContent")
            print(f"\n📊 Results counter: {results_h1}")
        except:
            print("\n⚠️  Could not find results counter")
        
        # Quick element count
        counts = await page.evaluate("""
            () => {
                return {
                    'h1': document.querySelectorAll('h1').length,
                    'h2': document.querySelectorAll('h2').length,
                    'h3': document.querySelectorAll('h3').length,
                    'article': document.querySelectorAll('article').length,
                    'li': document.querySelectorAll('li').length,
                    'div': document.querySelectorAll('div').length,
                    'a': document.querySelectorAll('a').length,
                    '[role="listitem"]': document.querySelectorAll('[role="listitem"]').length,
                    '[data-job-id]': document.querySelectorAll('[data-job-id]').length,
                };
            }
        """)
        
        print("\n📊 Element counts on page:")
        for tag, count in counts.items():
            if count > 0:
                print(f"   {tag}: {count}")
        
        print("\n" + "="*80)
        print("INSPECTION INSTRUCTIONS")
        print("="*80)
        print("""
Now you can manually inspect the page:

1. RIGHT-CLICK on a job title → Select "Inspect"
   
2. In DevTools, look at the HTML structure:
   - Find the container element for ONE job
   - Look for parent elements going up the tree
   
3. Note down these details:
   ┌─────────────────────────────────────────────┐
   │ Container Tag Name:  _________________      │
   │                     (div, li, article?)     │
   │                                             │
   │ Container Classes:   _________________      │
   │                     (job-card, ms-List?)    │
   │                                             │
   │ Data Attributes:     _________________      │
   │                     (data-job-id, etc.)     │
   │                                             │
   │ Job Title Tag:       _________________      │
   │                     (h2, h3, a?)            │
   │                                             │
   │ Job Title Classes:   _________________      │
   └─────────────────────────────────────────────┘

4. Example of what to look for:
   
   <div class="job-result-card" data-job-id="12345">  ← THIS IS THE CONTAINER!
       <h2 class="job-title">Senior AI Engineer</h2>  ← JOB TITLE
       <span class="location">Seattle, WA</span>      ← LOCATION
       <a href="/job/12345">View Details</a>          ← LINK
   </div>

5. Count how many job containers you see:
   - Are there 5 job containers matching your pattern?
   - Are they all visible on screen?

6. Try this in the Browser Console (F12 → Console tab):
   
   document.querySelectorAll('.YOUR_CLASS_HERE').length
   
   Replace .YOUR_CLASS_HERE with the actual class you found
   (e.g., '.job-result-card' or '[role="listitem"]')
   
   This will tell you how many elements match that selector.

""")
        
        print("="*80)
        print("⏸️  SCRIPT PAUSED - Browser will stay open")
        print("="*80)
        print("\nTake your time to inspect the elements.")
        print("When done, press Ctrl+C in this terminal to close the browser.\n")
        
        try:
            # Keep browser open until user interrupts
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("\n\n✅ Closing browser...")
        
        await browser.close()
        
        print("\n" + "="*80)
        print("NEXT STEPS")
        print("="*80)
        print("""
After inspecting, share what you found:

1. Container selector (e.g., ".job-card", "[role='listitem']")
2. Job title selector (e.g., "h2", ".job-title")
3. Number of jobs found with that selector

Then I'll update the scraper with the correct selectors!
""")


if __name__ == "__main__":
    try:
        asyncio.run(manual_inspection())
    except KeyboardInterrupt:
        print("\n\n👋 Manual inspection ended")
