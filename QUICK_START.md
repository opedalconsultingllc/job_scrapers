# Quick Start Guide 🚀

## Prerequisites Check
```bash
# Verify Python version
python --version  # Should be 3.12.11

# Activate virtual environment
source .venv/bin/activate
```

## Run Tests First (Recommended)
```bash
# Run all tests to verify everything works
pytest test_microsoft_scraper.py -v

# Should see: 13 passed ✅
```

## Run the Scraper

### Option 1: Use the Runner Script
```bash
python run_scraper.py
```

### Option 2: Custom Python Script
```python
import asyncio
from microsoft_scraper import MicrosoftCareersScraper

async def main():
    # Create scraper instance
    scraper = MicrosoftCareersScraper(
        headless=False  # Set to True to hide browser
    )
    
    # Scrape jobs
    jobs = await scraper.scrape(
        job_title="AI",           # Search term
        location="Seattle",        # Location filter
        max_jobs=50               # Max results to scrape
    )
    
    # Save results
    scraper.save_to_csv()  # Saves to output/microsoft_jobs_TIMESTAMP.csv
    scraper.save_to_json() # Saves to output/microsoft_jobs_TIMESTAMP.json
    
    # Print summary
    print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
    print(f"📁 Results saved to output/ directory")

if __name__ == "__main__":
    asyncio.run(main())
```

### Option 3: Interactive Python
```python
# Start Python in virtual environment
python

# Then in Python:
import asyncio
from microsoft_scraper import MicrosoftCareersScraper

scraper = MicrosoftCareersScraper(headless=False)
jobs = asyncio.run(scraper.scrape("AI", "Seattle", 10))
scraper.save_to_csv("ai_jobs_seattle.csv")
print(f"Found {len(jobs)} jobs")
```

## Expected Output

```
2025-10-03 10:30:15 - microsoft_scraper - INFO - Initializing browser with headless=False
2025-10-03 10:30:16 - microsoft_scraper - INFO - Browser initialized successfully
2025-10-03 10:30:17 - microsoft_scraper - INFO - Navigating to https://careers.microsoft.com/v2/global/en/home.html
2025-10-03 10:30:20 - microsoft_scraper - INFO - Successfully navigated to homepage
2025-10-03 10:30:21 - microsoft_scraper - INFO - Searching for: AI in Seattle
2025-10-03 10:30:25 - microsoft_scraper - INFO - Search completed successfully
2025-10-03 10:30:26 - microsoft_scraper - INFO - Scraping job listings (max: 50)
2025-10-03 10:30:28 - microsoft_scraper - INFO - Found 15 job listings with selector: article
2025-10-03 10:30:30 - microsoft_scraper - INFO - Scraped job 1/15: Senior AI Engineer
2025-10-03 10:30:32 - microsoft_scraper - INFO - Scraped job 2/15: Machine Learning Scientist
...
2025-10-03 10:31:10 - microsoft_scraper - INFO - Successfully scraped 15 jobs
2025-10-03 10:31:11 - microsoft_scraper - INFO - Saved 15 jobs to output/microsoft_jobs_20251003_103111.csv
2025-10-03 10:31:11 - microsoft_scraper - INFO - Saved 15 jobs to output/microsoft_jobs_20251003_103111.json
```

## Output Files

Results are saved in the `output/` directory:

```
output/
├── microsoft_jobs_20251003_103111.csv
└── microsoft_jobs_20251003_103111.json
```

### CSV Format
```csv
title,job_location,url,posted_date,description,scraped_at,source,search_term,location
Senior AI Engineer,Seattle WA,https://careers.microsoft.com/job/123,Posted 3 days ago,Lead AI initiatives...,2025-10-03T10:31:11,Microsoft Careers,AI,Seattle
```

### JSON Format
```json
[
  {
    "title": "Senior AI Engineer",
    "job_location": "Seattle, WA",
    "url": "https://careers.microsoft.com/job/123",
    "posted_date": "Posted 3 days ago",
    "description": "Lead AI initiatives...",
    "scraped_at": "2025-10-03T10:31:11",
    "source": "Microsoft Careers",
    "search_term": "AI",
    "location": "Seattle"
  }
]
```

## Common Commands

```bash
# Activate environment
source .venv/bin/activate

# Run tests
pytest test_microsoft_scraper.py -v

# Run scraper
python run_scraper.py

# Check output files
ls -lh output/

# View CSV results
cat output/microsoft_jobs_*.csv

# View JSON results (pretty-printed)
python -m json.tool output/microsoft_jobs_*.json

# Deactivate environment when done
deactivate
```

## Customization Tips

### Search Different Jobs
```python
jobs = await scraper.scrape("Machine Learning", "Redmond", 25)
```

### Run in Headless Mode (Faster)
```python
scraper = MicrosoftCareersScraper(headless=True)
```

### Custom Output Filename
```python
scraper.save_to_csv("my_custom_filename.csv")
scraper.save_to_json("my_custom_filename.json")
```

### Access Job Data
```python
jobs = await scraper.scrape("AI", "Seattle", 10)

for job in jobs:
    print(f"Title: {job['title']}")
    print(f"Location: {job['job_location']}")
    print(f"URL: {job['url']}")
    print(f"Posted: {job['posted_date']}")
    print("-" * 50)
```

## Troubleshooting

### Chromium notification pop-ups (macOS)
- ✅ **FIXED**: Notification pop-ups are now automatically blocked
- See `CHROMIUM_POPUPS_FIX.md` for details

### Search box not filling
- ✅ **FIXED**: Now targets the correct search box (`#search-box9`)
- See `SELECTOR_FIX.md` for details

### Browser doesn't open
- Check if Chromium is installed: `playwright install chromium`
- Try running in headless mode: `headless=True`

### No jobs found
- Check the search terms are correct
- Verify the Microsoft Careers site is accessible
- Review logs for specific errors

### Timeout errors
- Increase timeout in `config.py`
- Check internet connection
- Website structure may have changed

### Import errors
- Ensure virtual environment is activated
- Reinstall dependencies: `uv pip install -r requirements.txt`

## Best Practices

1. **Start Small**: Test with `max_jobs=5` first
2. **Monitor Behavior**: Run with `headless=False` initially
3. **Check Logs**: Review output for any warnings
4. **Respect Rate Limits**: Don't scrape too frequently
5. **Save Results**: Always save to files for later analysis

---

**Ready to scrape!** 🎉

Start with: `python run_scraper.py`
