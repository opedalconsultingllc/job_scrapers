#!/usr/bin/env python3
"""
Page Inspector - Captures actual element structures from Microsoft Careers
This will help us identify the correct selectors for location field and job listings.
"""

import asyncio
from playwright.async_api import async_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def inspect_page():
    """Inspect the Microsoft Careers page to find actual selectors."""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-notifications',
                '--disable-popup-blocking',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            permissions=[],
        )
        
        page = await context.new_page()
        
        print("\n" + "="*80)
        print("MICROSOFT CAREERS PAGE INSPECTOR")
        print("="*80 + "\n")
        
        # Navigate to homepage
        print("📍 Navigating to Microsoft Careers...")
        await page.goto("https://careers.microsoft.com/v2/global/en/home.html", wait_until='networkidle')
        await asyncio.sleep(3)
        
        print("✅ Page loaded!\n")
        
        # Inspect search box
        print("-" * 80)
        print("🔍 INSPECTING SEARCH BOX (Job Title Field)")
        print("-" * 80)
        
        search_box_script = """
        () => {
            const searchInputs = document.querySelectorAll('input[type="search"], input[role="searchbox"], input.ms-SearchBox-field, input[placeholder*="job"], input[placeholder*="keyword"]');
            const results = [];
            searchInputs.forEach((input, idx) => {
                results.push({
                    index: idx,
                    id: input.id || 'N/A',
                    class: input.className || 'N/A',
                    placeholder: input.placeholder || 'N/A',
                    ariaLabel: input.getAttribute('aria-label') || 'N/A',
                    name: input.name || 'N/A',
                    role: input.role || 'N/A',
                    type: input.type || 'N/A',
                });
            });
            return results;
        }
        """
        
        search_inputs = await page.evaluate(search_box_script)
        for inp in search_inputs:
            print(f"\nSearch Input #{inp['index']}:")
            print(f"  ID: {inp['id']}")
            print(f"  Class: {inp['class']}")
            print(f"  Placeholder: {inp['placeholder']}")
            print(f"  Aria-Label: {inp['ariaLabel']}")
            print(f"  Name: {inp['name']}")
            print(f"  Role: {inp['role']}")
            print(f"  Type: {inp['type']}")
        
        # Inspect location field
        print("\n" + "-" * 80)
        print("📍 INSPECTING LOCATION FIELD")
        print("-" * 80)
        
        location_script = """
        () => {
            const locationInputs = document.querySelectorAll('input[placeholder*="location"], input[placeholder*="city"], input[placeholder*="where"], input[aria-label*="location"]');
            const results = [];
            locationInputs.forEach((input, idx) => {
                results.push({
                    index: idx,
                    id: input.id || 'N/A',
                    class: input.className || 'N/A',
                    placeholder: input.placeholder || 'N/A',
                    ariaLabel: input.getAttribute('aria-label') || 'N/A',
                    name: input.name || 'N/A',
                    role: input.role || 'N/A',
                    type: input.type || 'N/A',
                    visible: window.getComputedStyle(input).display !== 'none'
                });
            });
            return results;
        }
        """
        
        location_inputs = await page.evaluate(location_script)
        if location_inputs:
            for inp in location_inputs:
                print(f"\nLocation Input #{inp['index']}:")
                print(f"  ID: {inp['id']}")
                print(f"  Class: {inp['class']}")
                print(f"  Placeholder: {inp['placeholder']}")
                print(f"  Aria-Label: {inp['ariaLabel']}")
                print(f"  Name: {inp['name']}")
                print(f"  Visible: {inp['visible']}")
        else:
            print("\n⚠️  No location inputs found! Microsoft might not have a separate location field.")
        
        # Inspect search button
        print("\n" + "-" * 80)
        print("🔘 INSPECTING SEARCH BUTTON")
        print("-" * 80)
        
        button_script = """
        () => {
            const buttons = document.querySelectorAll('button[type="submit"], button.search-button, button[aria-label*="search"], button[aria-label*="find"]');
            const results = [];
            buttons.forEach((btn, idx) => {
                results.push({
                    index: idx,
                    id: btn.id || 'N/A',
                    class: btn.className || 'N/A',
                    text: btn.textContent.trim(),
                    ariaLabel: btn.getAttribute('aria-label') || 'N/A',
                    type: btn.type || 'N/A',
                });
            });
            return results;
        }
        """
        
        buttons = await page.evaluate(button_script)
        for btn in buttons:
            print(f"\nButton #{btn['index']}:")
            print(f"  ID: {btn['id']}")
            print(f"  Class: {btn['class']}")
            print(f"  Text: {btn['text']}")
            print(f"  Aria-Label: {btn['ariaLabel']}")
            print(f"  Type: {btn['type']}")
        
        # Now fill in the search and wait for results
        print("\n" + "="*80)
        print("🔍 PERFORMING SEARCH FOR 'AI'")
        print("="*80 + "\n")
        
        # Fill search box
        search_box = await page.query_selector('#search-box9')
        if search_box:
            await search_box.fill('AI')
            print("✅ Filled search box with 'AI'")
            await asyncio.sleep(1)
            
            # Press Enter to search
            await page.keyboard.press('Enter')
            print("✅ Pressed Enter to search")
            
            # Wait for results
            print("⏳ Waiting for results to load...")
            await page.wait_for_load_state('networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            print("✅ Results loaded!\n")
        
        # Inspect job listing elements
        print("-" * 80)
        print("📋 INSPECTING JOB LISTINGS ON RESULTS PAGE")
        print("-" * 80)
        
        job_listings_script = """
        () => {
            const results = {
                articles: document.querySelectorAll('article').length,
                jobListings: document.querySelectorAll('.job-listing').length,
                jobItems: document.querySelectorAll('.job-item').length,
                jobCards: document.querySelectorAll('.job-card').length,
                dataJobId: document.querySelectorAll('[data-job-id]').length,
                roleArticle: document.querySelectorAll('[role="article"]').length,
                allDivs: document.querySelectorAll('div[class*="job"]').length,
            };
            
            // Get sample structure of first few elements
            const samples = [];
            
            // Try to find any job-related container
            const possibleContainers = document.querySelectorAll('[class*="job"], [data-job], [class*="result"]');
            
            for (let i = 0; i < Math.min(3, possibleContainers.length); i++) {
                const elem = possibleContainers[i];
                samples.push({
                    tagName: elem.tagName,
                    className: elem.className,
                    id: elem.id || 'N/A',
                    dataAttributes: Array.from(elem.attributes)
                        .filter(attr => attr.name.startsWith('data-'))
                        .map(attr => `${attr.name}="${attr.value}"`).join(', ') || 'N/A',
                    innerHTML: elem.innerHTML.substring(0, 200) + '...'
                });
            }
            
            return { counts: results, samples: samples };
        }
        """
        
        job_data = await page.evaluate(job_listings_script)
        
        print("\n📊 Job Listing Counts:")
        for selector, count in job_data['counts'].items():
            print(f"  {selector}: {count}")
        
        print("\n📝 Sample Job Elements (first 3):")
        for idx, sample in enumerate(job_data['samples'], 1):
            print(f"\nSample #{idx}:")
            print(f"  Tag: {sample['tagName']}")
            print(f"  Class: {sample['className']}")
            print(f"  ID: {sample['id']}")
            print(f"  Data Attributes: {sample['dataAttributes']}")
            print(f"  Inner HTML Preview: {sample['innerHTML'][:150]}...")
        
        # Get detailed structure of first job listing
        print("\n" + "-" * 80)
        print("🔬 DETAILED STRUCTURE OF FIRST JOB LISTING")
        print("-" * 80)
        
        detailed_job_script = """
        () => {
            // Find the most likely job container
            const container = document.querySelector('[class*="job"]') || 
                            document.querySelector('[data-job]') ||
                            document.querySelector('article') ||
                            document.querySelector('[class*="result"]');
            
            if (!container) return null;
            
            return {
                outerHTML: container.outerHTML.substring(0, 500),
                classes: container.className,
                // Find title elements
                titles: Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6, [class*="title"]')).map(el => ({
                    tag: el.tagName,
                    class: el.className,
                    text: el.textContent.trim().substring(0, 100)
                })),
                // Find location elements
                locations: Array.from(container.querySelectorAll('[class*="location"], [class*="city"]')).map(el => ({
                    tag: el.tagName,
                    class: el.className,
                    text: el.textContent.trim()
                })),
                // Find links
                links: Array.from(container.querySelectorAll('a')).map(el => ({
                    class: el.className,
                    href: el.href,
                    text: el.textContent.trim().substring(0, 50)
                }))
            };
        }
        """
        
        detailed_job = await page.evaluate(detailed_job_script)
        
        if detailed_job:
            print("\n📦 Container:")
            print(f"  Classes: {detailed_job['classes']}")
            print(f"\n  HTML Preview:\n{detailed_job['outerHTML']}...\n")
            
            print("📌 Title Elements Found:")
            for title in detailed_job['titles']:
                print(f"  - {title['tag']}.{title['class']}: {title['text']}")
            
            print("\n📍 Location Elements Found:")
            for loc in detailed_job['locations']:
                print(f"  - {loc['tag']}.{loc['class']}: {loc['text']}")
            
            print("\n🔗 Links Found:")
            for link in detailed_job['links'][:3]:  # First 3 links
                print(f"  - {link['class']}: {link['text']}")
                print(f"    URL: {link['href']}")
        else:
            print("\n⚠️  Could not find any job listing container!")
        
        print("\n" + "="*80)
        print("🎯 RECOMMENDED SELECTORS")
        print("="*80 + "\n")
        
        # Generate recommendations
        if search_inputs:
            print("Job Title Field:")
            print(f"  Primary: #{search_inputs[0]['id']}")
            print(f"  Backup: .{search_inputs[0]['class'].split()[0] if search_inputs[0]['class'] != 'N/A' else 'ms-SearchBox-field'}")
        
        if location_inputs:
            print("\nLocation Field:")
            print(f"  Primary: #{location_inputs[0]['id']}")
            print(f"  Backup: input[placeholder*='{location_inputs[0]['placeholder'][:20]}']")
        else:
            print("\n⚠️  No location field - Microsoft might use a different approach")
        
        if detailed_job and detailed_job['classes']:
            print("\nJob Listing Container:")
            main_class = detailed_job['classes'].split()[0] if detailed_job['classes'] else 'unknown'
            print(f"  Primary: .{main_class}")
            print(f"  Backup: [class*='{main_class[:10]}']")
        
        print("\n" + "="*80)
        print("✅ INSPECTION COMPLETE - Browser will stay open for 30 seconds")
        print("   You can manually inspect elements if needed.")
        print("="*80 + "\n")
        
        # Keep browser open for inspection
        await asyncio.sleep(30)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(inspect_page())
