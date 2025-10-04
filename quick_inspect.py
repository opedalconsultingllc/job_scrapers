#!/usr/bin/env python3
"""
Quick Page Inspector - Captures element info and saves to file
"""

import asyncio
from playwright.async_api import async_playwright
import json


async def quick_inspect():
    """Quick inspection of Microsoft Careers page."""
    
    output = {
        'search_fields': [],
        'location_fields': [],
        'buttons': [],
        'job_listings': {},
        'recommendations': {}
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-notifications', '--disable-popup-blocking']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            permissions=[],
        )
        
        page = await context.new_page()
        
        # Navigate
        await page.goto("https://careers.microsoft.com/v2/global/en/home.html", wait_until='networkidle')
        await asyncio.sleep(3)
        
        # Get search fields
        search_inputs = await page.evaluate("""
            () => {
                const inputs = document.querySelectorAll('input');
                return Array.from(inputs).map(input => ({
                    id: input.id,
                    class: input.className,
                    placeholder: input.placeholder,
                    ariaLabel: input.getAttribute('aria-label'),
                    type: input.type,
                    name: input.name
                })).filter(i => i.id || i.placeholder || i.ariaLabel);
            }
        """)
        output['search_fields'] = search_inputs
        
        # Fill search and submit
        await page.fill('#search-box9', 'AI')
        await asyncio.sleep(1)
        await page.keyboard.press('Enter')
        await page.wait_for_load_state('networkidle', timeout=30000)
        await asyncio.sleep(5)
        
        # Get all possible job containers
        job_info = await page.evaluate("""
            () => {
                const info = {
                    selectors: {
                        'article': document.querySelectorAll('article').length,
                        '[class*="job"]': document.querySelectorAll('[class*="job"]').length,
                        '[data-job-id]': document.querySelectorAll('[data-job-id]').length,
                        '[role="listitem"]': document.querySelectorAll('[role="listitem"]').length,
                        'li': document.querySelectorAll('li').length,
                        'ul > *': document.querySelectorAll('ul > *').length,
                    },
                    sample: null
                };
                
                // Find first job-like element
                const firstJob = document.querySelector('[class*="job"]') || 
                                document.querySelector('article') ||
                                document.querySelector('[role="listitem"]') ||
                                document.querySelector('ul > li');
                
                if (firstJob) {
                    info.sample = {
                        tag: firstJob.tagName,
                        classes: firstJob.className,
                        id: firstJob.id,
                        innerHTML: firstJob.innerHTML.substring(0, 800),
                        children: Array.from(firstJob.children).map(child => ({
                            tag: child.tagName,
                            class: child.className,
                            text: child.textContent.trim().substring(0, 100)
                        }))
                    };
                }
                
                return info;
            }
        """)
        output['job_listings'] = job_info
        
        await browser.close()
    
    # Save to file
    with open('page_inspection_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n✅ Inspection complete! Results saved to: page_inspection_results.json")
    print("\nKey findings:")
    print(f"- Found {len(output['search_fields'])} input fields")
    print(f"- Job listings found with selectors:")
    for selector, count in output['job_listings']['selectors'].items():
        if count > 0:
            print(f"  • {selector}: {count} elements")
    
    if output['job_listings'].get('sample'):
        sample = output['job_listings']['sample']
        print(f"\nFirst job element:")
        print(f"  Tag: {sample['tag']}")
        print(f"  Classes: {sample['classes'][:100]}")


if __name__ == "__main__":
    asyncio.run(quick_inspect())
