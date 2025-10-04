#!/usr/bin/env python3
"""
Quick runner script for Microsoft Careers Scraper
"""

import asyncio
import sys
from pathlib import Path

from microsoft_scraper import MicrosoftCareersScraper
from config import SCRAPER_CONFIG


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print(" " * 15 + "MICROSOFT CAREERS SCRAPER")
    print("="*70 + "\n")


def print_menu():
    """Print interactive menu."""
    print("Select an option:")
    print("1. Scrape AI jobs in Seattle (default)")
    print("2. Custom search")
    print("3. Run tests")
    print("4. Exit")
    print()


async def scrape_with_config(job_title: str, location: str, max_jobs: int, headless: bool = False):
    """
    Run scraper with given configuration.
    
    Args:
        job_title: Job title to search for
        location: Location to search in
        max_jobs: Maximum number of jobs to scrape
        headless: Whether to run in headless mode
    """
    print(f"\n🔍 Searching for '{job_title}' jobs in '{location}'...")
    print(f"📊 Max jobs to scrape: {max_jobs}")
    print(f"🤖 Headless mode: {headless}")
    print("\n" + "-"*70 + "\n")
    
    scraper = MicrosoftCareersScraper(headless=headless)
    
    try:
        jobs = await scraper.scrape(
            job_title=job_title,
            location=location,
            max_jobs=max_jobs
        )
        
        if jobs:
            print("\n" + "="*70)
            print(f"✅ Successfully scraped {len(jobs)} jobs!")
            print("="*70 + "\n")
            
            # Display sample jobs
            sample_size = min(5, len(jobs))
            print(f"📋 Sample of {sample_size} jobs:\n")
            
            for idx, job in enumerate(jobs[:sample_size], 1):
                print(f"{idx}. {job.get('title', 'N/A')}")
                print(f"   📍 Location: {job.get('job_location', 'N/A')}")
                print(f"   📅 Posted: {job.get('posted_date', 'N/A')}")
                print(f"   🔗 URL: {job.get('url', 'N/A')[:60]}...")
                print()
            
            # Save results
            print("💾 Saving results...")
            scraper.save_to_csv()
            scraper.save_to_json()
            
            print("\n✨ Done! Check the 'output' directory for results.\n")
        else:
            print("\n❌ No jobs were scraped. Please check the logs for errors.\n")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user.\n")
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}\n")
        raise


async def run_default_scrape():
    """Run scraper with default configuration."""
    await scrape_with_config(
        job_title=SCRAPER_CONFIG['default_job_title'],
        location=SCRAPER_CONFIG['default_location'],
        max_jobs=SCRAPER_CONFIG['max_jobs'],
        headless=SCRAPER_CONFIG['headless']
    )


async def run_custom_scrape():
    """Run scraper with custom user input."""
    print("\n📝 Custom Search Configuration\n")
    
    job_title = input("Enter job title (default: AI): ").strip() or "AI"
    location = input("Enter location (default: Seattle): ").strip() or "Seattle"
    
    try:
        max_jobs = input("Enter max jobs to scrape (default: 50): ").strip()
        max_jobs = int(max_jobs) if max_jobs else 50
    except ValueError:
        print("Invalid number, using default (50)")
        max_jobs = 50
    
    headless_input = input("Run in headless mode? (y/N): ").strip().lower()
    headless = headless_input in ['y', 'yes']
    
    await scrape_with_config(
        job_title=job_title,
        location=location,
        max_jobs=max_jobs,
        headless=headless
    )


def run_tests():
    """Run the test suite."""
    import subprocess
    
    print("\n🧪 Running test suite...\n")
    print("-"*70 + "\n")
    
    try:
        result = subprocess.run(
            ['pytest', 'test_microsoft_scraper.py', '-v'],
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("\n✅ All tests passed!\n")
        else:
            print("\n❌ Some tests failed. Please review the output above.\n")
            
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest\n")
    except Exception as e:
        print(f"❌ Error running tests: {e}\n")


async def interactive_mode():
    """Run in interactive mode with menu."""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            await run_default_scrape()
            input("\nPress Enter to continue...")
            print("\n")
            
        elif choice == '2':
            await run_custom_scrape()
            input("\nPress Enter to continue...")
            print("\n")
            
        elif choice == '3':
            run_tests()
            input("\nPress Enter to continue...")
            print("\n")
            
        elif choice == '4':
            print("\n👋 Goodbye!\n")
            break
            
        else:
            print("\n❌ Invalid choice. Please try again.\n")


def main():
    """Main entry point."""
    try:
        # Check if running with command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == '--test':
                run_tests()
            elif sys.argv[1] == '--quick':
                asyncio.run(run_default_scrape())
            elif sys.argv[1] == '--help':
                print("\nUsage:")
                print("  python run_scraper.py           # Interactive mode")
                print("  python run_scraper.py --quick   # Quick run with defaults")
                print("  python run_scraper.py --test    # Run tests")
                print("  python run_scraper.py --help    # Show this help")
                print()
            else:
                print(f"Unknown argument: {sys.argv[1]}")
                print("Use --help for usage information")
        else:
            # Interactive mode
            asyncio.run(interactive_mode())
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
