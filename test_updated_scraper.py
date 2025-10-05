#!/usr/bin/env python3
"""
Quick test with the updated selectors
"""

import asyncio
from microsoft_scraper import MicrosoftCareersScraper


async def test_scraper():
    """Test the scraper with correct selectors."""
    
    print("\n" + "="*80)
    print("TESTING UPDATED SCRAPER WITH CORRECT SELECTORS")
    print("="*80 + "\n")
    
    print("🎯 Using selectors from manual inspection:")
    print("   - Container: div.ms-List-cell[role='listitem']")
    print("   - Title: h2.MZGzlrn8gfgSs8TZHhv2")
    print("   - Location: i[data-icon-name='POI'] + span")
    print("   - Date: i[data-icon-name='Clock'] + span")
    print("   - Description: span[aria-label='job description']")
    print("   - Job ID: from aria-label 'Job item XXXXX'\n")
    
    scraper = MicrosoftCareersScraper(headless=False)
    
    try:
        print("🔍 Scraping 5 AI jobs...\n")
        jobs = await scraper.scrape(
            job_title="AI",
            location="Seattle", 
            max_jobs=5
        )
        
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80 + "\n")
        
        if jobs:
            print(f"✅ Successfully scraped {len(jobs)} jobs!\n")
            
            for idx, job in enumerate(jobs, 1):
                print(f"Job {idx}:")
                print(f"  📌 Title: {job.get('title', 'N/A')}")
                print(f"  📍 Location: {job.get('job_location', 'N/A')}")
                print(f"  📅 Posted: {job.get('posted_date', 'N/A')}")
                print(f"  🔗 URL: {job.get('url', 'N/A')[:80]}")
                if job.get('job_id'):
                    print(f"  🆔 Job ID: {job.get('job_id')}")
                desc = job.get('description', 'N/A')
                print(f"  📝 Description: {desc[:100]}..." if len(desc) > 100 else f"  📝 Description: {desc}")
                print()
            
            # Save results
            print("💾 Saving results...")
            scraper.save_to_csv("test_results.csv")
            scraper.save_to_json("test_results.json")
            print("✅ Saved to output/test_results.csv and output/test_results.json")
            
        else:
            print("❌ No jobs were scraped!")
            print("\n📋 Check the logs above for details on what went wrong.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_scraper())
