# Microsoft Careers Scraper - Setup Complete ✅

## Environment Setup

### Python Version
- **Python 3.12.11** installed and configured via `uv`
- Virtual environment created at `.venv/`

### Dependencies Installed
All required packages have been installed in the virtual environment:
- ✅ playwright (1.55.0)
- ✅ pandas (2.3.3)
- ✅ python-dotenv (1.1.1)
- ✅ pytest (8.4.2)
- ✅ pytest-asyncio (1.2.0)
- ✅ tenacity (9.1.2)

### Playwright Browsers
- ✅ Chromium browser installed and ready

## Project Structure

```
job_scrapers/
├── microsoft_scraper.py          # Main scraper implementation
├── test_microsoft_scraper.py     # Comprehensive test suite (13 tests)
├── run_scraper.py               # Simple runner script
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
├── README.md                   # Main documentation
├── SCRAPER_README.md          # Scraper-specific docs
└── .venv/                     # Virtual environment (Python 3.12)
```

## Test Results

All tests passing: **13/13 ✅**

### Test Coverage
1. ✅ Human behavior simulation (random delays, typing, clicking)
2. ✅ Browser initialization and configuration
3. ✅ Page navigation
4. ✅ Search form interaction
5. ✅ Job listing scraping
6. ✅ Cookie consent handling
7. ✅ CSV export
8. ✅ JSON export
9. ✅ Retry/timeout behavior
10. ✅ End-to-end mock scraping

## Features Implemented

### Human-Like Behavior
- ✅ Random delays between actions
- ✅ Character-by-character typing with variable speed
- ✅ Mouse movement simulation
- ✅ Random scrolling patterns

### Backoff Strategies
- ✅ Exponential backoff with tenacity
- ✅ Configurable retry attempts
- ✅ Smart timeout handling
- ✅ Error recovery mechanisms

### Scraping Capabilities
- ✅ Search by job title (AI)
- ✅ Filter by location (Seattle)
- ✅ Extract job details (title, location, URL, date, description)
- ✅ Handle pagination
- ✅ Cookie consent management

### Data Export
- ✅ Save to CSV format
- ✅ Save to JSON format
- ✅ Timestamped filenames
- ✅ Organized output directory

## How to Use

### Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Run Tests
```bash
pytest test_microsoft_scraper.py -v
```

### Run the Scraper
```bash
python run_scraper.py
```

Or use it programmatically:
```python
import asyncio
from microsoft_scraper import MicrosoftCareersScraper

async def main():
    scraper = MicrosoftCareersScraper(headless=False)  # Set to True for headless
    jobs = await scraper.scrape(
        job_title="AI",
        location="Seattle",
        max_jobs=50
    )
    
    scraper.save_to_csv()
    scraper.save_to_json()
    
    print(f"Scraped {len(jobs)} jobs!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

Edit `config.py` to customize:
- User agent strings
- Viewport sizes
- Timeout durations
- Delay ranges
- Output directories
- Retry strategies

## Safety Features

1. **Rate Limiting**: Built-in delays between requests
2. **Human Behavior**: Mimics real user interactions
3. **Error Handling**: Graceful failure and recovery
4. **Logging**: Comprehensive logging for debugging
5. **Respectful Scraping**: Follows best practices

## Next Steps

### Ready to Scrape!
The scraper is fully tested and ready to use on the actual Microsoft Careers website:
- Target URL: https://careers.microsoft.com/v2/global/en/home.html
- Search term: AI
- Location: Seattle

### Before Running on Production
1. Review `config.py` settings
2. Consider running in headless mode: `headless=True`
3. Monitor the logs for any issues
4. Start with a small `max_jobs` value to test
5. Gradually increase as needed

### Recommended First Run
```bash
# Run with visible browser to observe behavior
python run_scraper.py
```

## Troubleshooting

### If you need to reinstall dependencies
```bash
uv pip install -r requirements.txt
```

### If Playwright browsers are missing
```bash
playwright install chromium
```

### Check Python version
```bash
python --version  # Should show Python 3.12.11
```

## Notes

- The scraper uses Playwright in headed mode by default to observe behavior
- All tests use headless mode for speed
- Output files are saved to the `output/` directory
- Logs provide detailed information about scraping progress
- The scraper is designed to be respectful and avoid overwhelming the server

---

**Setup completed successfully on October 3, 2025**

Managed by: `uv` package manager
Python Version: 3.12.11
All dependencies installed and tested ✅
