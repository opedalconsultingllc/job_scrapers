# Job Scrapers

A collection of web scrapers for job posting websites with human-like behavior and robust error handling.

## 🚀 Quick Start

1. **Create and activate virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

3. **Run tests first:**
```bash
pytest test_microsoft_scraper.py -v
```

4. **Run the scraper:**
```bash
# Interactive mode
python run_scraper.py

# Quick run with defaults
python run_scraper.py --quick

# Run tests
python run_scraper.py --test
```

## 📦 Available Scrapers

### Microsoft Careers Scraper
Scrapes AI job listings from Microsoft Careers website.

**Features:**
- ✅ Playwright-based with headed browser
- ✅ Human-like behavior (random delays, realistic typing)
- ✅ Exponential backoff retry strategy
- ✅ Anti-detection measures
- ✅ Comprehensive test suite
- ✅ CSV and JSON export

**Files:**
- `microsoft_scraper.py` - Main scraper implementation
- `test_microsoft_scraper.py` - Test suite
- `run_scraper.py` - Interactive runner
- `config.py` - Configuration settings
- `SCRAPER_README.md` - Detailed documentation

## 🧪 Testing

Always run tests before scraping the actual site:

```bash
# Run all tests
pytest test_microsoft_scraper.py -v

# Run specific test
pytest test_microsoft_scraper.py::test_end_to_end_mock_scrape -v

# Run with output
pytest test_microsoft_scraper.py -v -s
```

## 📊 Usage Examples

### Interactive Mode
```bash
python run_scraper.py
```
Follow the menu prompts to:
1. Run with default settings (AI jobs in Seattle)
2. Custom search with your parameters
3. Run test suite
4. Exit

### Programmatic Usage
```python
import asyncio
from microsoft_scraper import MicrosoftCareersScraper

async def main():
    scraper = MicrosoftCareersScraper(headless=False)
    jobs = await scraper.scrape(
        job_title="AI",
        location="Seattle",
        max_jobs=50
    )
    
    if jobs:
        scraper.save_to_csv()
        scraper.save_to_json()

asyncio.run(main())
```

## 📁 Output

Scraped data is saved to the `output/` directory:
- `microsoft_ai_jobs_YYYYMMDD_HHMMSS.csv`
- `microsoft_ai_jobs_YYYYMMDD_HHMMSS.json`

## ⚙️ Configuration

Edit `config.py` to customize:
- Browser settings (headless mode, viewport, user agent)
- Timing delays (human-like behavior)
- Retry strategies (max attempts, backoff)
- Selectors (if website structure changes)
- Output formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
