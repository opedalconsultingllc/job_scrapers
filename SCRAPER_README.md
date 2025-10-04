# Microsoft Careers Scraper

This scraper collects AI job listings from Microsoft Careers using Playwright with human-like behavior and backoff strategies.

## Features

- **Playwright-based scraping**: Uses headed browser mode to mimic real user interaction
- **Human-like behavior**: 
  - Random delays between actions
  - Character-by-character typing with random speeds
  - Random mouse movements
  - Realistic viewport and user agent
- **Retry logic**: Automatic retry with exponential backoff on failures
- **Anti-detection**: Browser fingerprint masking and realistic settings
- **Data export**: Save results to CSV or JSON format

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Project Structure

```
job_scrapers/
├── microsoft_scraper.py          # Main scraper implementation
├── test_microsoft_scraper.py     # Comprehensive test suite
├── requirements.txt              # Python dependencies
└── output/                       # Scraped data (auto-created)
    ├── microsoft_ai_jobs_*.csv
    └── microsoft_ai_jobs_*.json
```

## Usage

### Run the Scraper

```bash
# Run with headed browser (default)
python microsoft_scraper.py
```

### Run Tests First

Before running on the actual site, test with mocked data:

```bash
# Run all tests
pytest test_microsoft_scraper.py -v

# Run specific test
pytest test_microsoft_scraper.py::test_end_to_end_mock_scrape -v

# Run with detailed output
pytest test_microsoft_scraper.py -v -s
```

### Programmatic Usage

```python
import asyncio
from microsoft_scraper import MicrosoftCareersScraper

async def scrape_jobs():
    # Initialize scraper
    scraper = MicrosoftCareersScraper(headless=False)
    
    # Scrape jobs
    jobs = await scraper.scrape(
        job_title="AI",
        location="Seattle",
        max_jobs=50
    )
    
    # Save results
    if jobs:
        scraper.save_to_csv()
        scraper.save_to_json()
        print(f"Scraped {len(jobs)} jobs!")

# Run
asyncio.run(scrape_jobs())
```

## Configuration

### Scraper Parameters

```python
scraper = MicrosoftCareersScraper(
    headless=False  # Set to True for headless mode
)

jobs = await scraper.scrape(
    job_title="AI",           # Search term
    location="Seattle",        # Location
    max_jobs=50               # Max results to scrape
)
```

### Human Behavior Settings

Modify timing in `HumanBehavior` class:

```python
# Adjust delays (in seconds)
await HumanBehavior.random_delay(
    min_seconds=1.0,    # Minimum delay
    max_seconds=3.0     # Maximum delay
)
```

### Retry Configuration

Adjust retry behavior in decorators:

```python
@retry(
    stop=stop_after_attempt(3),           # Max 3 attempts
    wait=wait_exponential(                # Exponential backoff
        multiplier=2,                     # 2x multiplier
        min=4,                            # Min 4 seconds
        max=30                            # Max 30 seconds
    )
)
```

## Output Format

### CSV Format
```csv
title,job_location,url,posted_date,description,scraped_at,source,search_term,location
"AI Engineer","Seattle, WA","/jobs/123","2 days ago","...",2025-10-03T10:30:00,Microsoft Careers,AI,Seattle
```

### JSON Format
```json
[
  {
    "title": "AI Engineer",
    "job_location": "Seattle, WA",
    "url": "/jobs/123",
    "posted_date": "2 days ago",
    "description": "...",
    "scraped_at": "2025-10-03T10:30:00",
    "source": "Microsoft Careers",
    "search_term": "AI",
    "location": "Seattle"
  }
]
```

## Testing

The test suite includes:

- **Unit tests**: Test individual components
- **Integration tests**: Test component interactions
- **Mock tests**: Test with simulated web pages
- **End-to-end tests**: Complete workflow testing

### Test Categories

1. **HumanBehavior Tests**: Verify human-like interactions
2. **Scraper Initialization**: Test browser setup
3. **Navigation Tests**: Test page navigation
4. **Search Tests**: Test form interactions
5. **Scraping Tests**: Test data extraction
6. **Export Tests**: Test file saving
7. **Retry Tests**: Test error handling

## Best Practices

1. **Always run tests first**: Validate functionality before scraping live site
2. **Use headed mode initially**: Watch the browser to debug issues
3. **Respect rate limits**: Built-in delays help avoid detection
4. **Handle errors gracefully**: Retry logic handles temporary failures
5. **Review scraped data**: Check output files for quality

## Troubleshooting

### Browser doesn't launch
```bash
# Reinstall Playwright browsers
playwright install chromium --force
```

### Selectors not found
The scraper uses multiple fallback selectors. If still failing:
1. Run in headed mode to inspect the page
2. Update selectors in the scraper code
3. Check if site structure changed

### Timeout errors
Increase timeout values or check internet connection:
```python
await page.goto(url, timeout=60000)  # 60 seconds
```

### No jobs found
1. Verify search works manually on the site
2. Check if selectors match current page structure
3. Review logs for detailed error messages

## Logging

The scraper uses Python's logging module:

```python
import logging

# Change log level
logging.basicConfig(level=logging.DEBUG)  # More verbose
logging.basicConfig(level=logging.INFO)   # Default
logging.basicConfig(level=logging.WARNING)  # Less verbose
```

## License

MIT License

## Notes

- The scraper is designed for educational purposes
- Always review and comply with website terms of service
- Use responsibly and ethically
- Consider API access if available
