#!/usr/bin/env python3
"""
Job Element Inspector - Finds and analyzes actual job listing elements
"""

import asyncio
from playwright.async_api import async_playwright
import json


async def inspect_job_elements():
    """Inspect actual job listing elements on results page."""
    
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
        
        print("\n" + "="*80)
        print("JOB ELEMENT STRUCTURE INSPECTOR")
        print("="*80 + "\n")
        
        # Navigate
        print("📍 Navigating to Microsoft Careers...")
        await page.goto("https://careers.microsoft.com/v2/global/en/home.html", wait_until='networkidle')
        await asyncio.sleep(3)
        
        # Fill search
        print("🔍 Searching for 'AI' jobs...")
        await page.fill('#search-box9', 'AI')
        await asyncio.sleep(1)
        await page.keyboard.press('Enter')
        await page.wait_for_load_state('networkidle', timeout=30000)
        await asyncio.sleep(5)
        
        print("✅ Results page loaded!\n")
        
        # Find the results counter
        results_text = await page.evaluate("""
            () => {
                const h1 = document.querySelector('h1');
                return h1 ? h1.textContent : 'Not found';
            }
        """)
        print(f"📊 Results counter: {results_text}\n")
        
        # Get comprehensive page structure
        page_structure = await page.evaluate("""
            () => {
                const results = {
                    h1Text: document.querySelector('h1')?.textContent || 'N/A',
                    allElements: {},
                    jobElements: []
                };
                
                // Count all possible job containers
                const selectors = [
                    'article',
                    '[role="listitem"]',
                    '[data-job-id]',
                    'li',
                    '[class*="job"]',
                    '[class*="result"]',
                    '[class*="card"]',
                    'ul > *',
                    '[role="list"] > *'
                ];
                
                selectors.forEach(sel => {
                    const count = document.querySelectorAll(sel).length;
                    if (count > 0) {
                        results.allElements[sel] = count;
                    }
                });
                
                // Find elements near the h1 (likely job containers)
                const h1 = document.querySelector('h1');
                if (h1) {
                    // Look at siblings and nearby elements
                    let parent = h1.parentElement;
                    for (let i = 0; i < 5 && parent; i++) {
                        parent = parent.parentElement;
                    }
                    
                    if (parent) {
                        // Get all children of this parent that might be jobs
                        const children = Array.from(parent.querySelectorAll('*'));
                        const jobLike = children.filter(el => {
                            const text = el.textContent || '';
                            const classes = el.className || '';
                            // Elements that contain substantial text and look job-like
                            return text.length > 50 && text.length < 2000 &&
                                   (classes.includes('job') || 
                                    classes.includes('result') || 
                                    classes.includes('card') ||
                                    classes.includes('item') ||
                                    el.tagName === 'LI' ||
                                    el.tagName === 'ARTICLE');
                        });
                        
                        results.jobElements = jobLike.slice(0, 3).map(el => ({
                            tag: el.tagName,
                            classes: el.className,
                            id: el.id || 'N/A',
                            dataAttrs: Array.from(el.attributes)
                                .filter(attr => attr.name.startsWith('data-'))
                                .map(attr => `${attr.name}="${attr.value}"`),
                            childrenTags: Array.from(el.children).map(c => c.tagName),
                            textPreview: el.textContent.substring(0, 200).trim(),
                            innerHTML: el.innerHTML.substring(0, 1000)
                        }));
                    }
                }
                
                // Also try to find any clickable job titles
                const links = Array.from(document.querySelectorAll('a'));
                const jobLinks = links.filter(a => {
                    const text = a.textContent?.trim() || '';
                    const href = a.href || '';
                    return text.length > 10 && 
                           text.length < 150 && 
                           (href.includes('job') || href.includes('careers'));
                }).slice(0, 5);
                
                results.jobLinks = jobLinks.map(a => ({
                    text: a.textContent.trim().substring(0, 100),
                    href: a.href,
                    parentTag: a.parentElement?.tagName,
                    parentClass: a.parentElement?.className
                }));
                
                return results;
            }
        """)
        
        # Print findings
        print("="*80)
        print("ELEMENT COUNTS")
        print("="*80)
        for selector, count in page_structure['allElements'].items():
            print(f"  {selector}: {count} elements")
        
        print("\n" + "="*80)
        print("JOB-LIKE ELEMENTS (Found near results)")
        print("="*80)
        
        if page_structure['jobElements']:
            for idx, elem in enumerate(page_structure['jobElements'], 1):
                print(f"\nElement #{idx}:")
                print(f"  Tag: {elem['tag']}")
                print(f"  Classes: {elem['classes'][:100]}")
                print(f"  ID: {elem['id']}")
                print(f"  Data Attributes: {elem['dataAttrs']}")
                print(f"  Children: {elem['childrenTags'][:10]}")
                print(f"  Text Preview: {elem['textPreview']}")
                print(f"\n  HTML Preview:")
                print(f"  {elem['innerHTML'][:500]}...")
        else:
            print("\n⚠️  No job-like elements found automatically!")
        
        print("\n" + "="*80)
        print("JOB LINKS (Potential job titles)")
        print("="*80)
        
        if page_structure.get('jobLinks'):
            for idx, link in enumerate(page_structure['jobLinks'], 1):
                print(f"\nLink #{idx}:")
                print(f"  Text: {link['text']}")
                print(f"  URL: {link['href']}")
                print(f"  Parent: {link['parentTag']}.{link['parentClass'][:50]}")
        
        # Take a screenshot for visual reference
        await page.screenshot(path='job_results_screenshot.png', full_page=True)
        print("\n📸 Screenshot saved: job_results_screenshot.png")
        
        # Save detailed results
        with open('job_elements_analysis.json', 'w') as f:
            json.dump(page_structure, f, indent=2)
        print("💾 Detailed analysis saved: job_elements_analysis.json")
        
        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)
        
        if page_structure['jobElements']:
            first = page_structure['jobElements'][0]
            print(f"\n✅ Found job elements!")
            print(f"   Recommended selector: {first['tag'].lower()}")
            if first['classes']:
                first_class = first['classes'].split()[0]
                print(f"   Alternative: .{first_class}")
        
        if page_structure.get('jobLinks'):
            first_link = page_structure['jobLinks'][0]
            print(f"\n✅ Found job links!")
            print(f"   Parent container: {first_link['parentTag']}")
            if first_link['parentClass']:
                print(f"   Parent class: {first_link['parentClass'][:50]}")
        
        print("\n" + "="*80)
        print("Browser will stay open for 30 seconds for manual inspection...")
        print("="*80)
        
        await asyncio.sleep(30)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(inspect_job_elements())
