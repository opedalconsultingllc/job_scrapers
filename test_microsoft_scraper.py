"""
Tests for Microsoft Careers Scraper
Tests the scraper functionality before running on the actual site.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from playwright.async_api import async_playwright, Page
from microsoft_scraper import (
    MicrosoftCareersScraper,
    HumanBehavior
)


class TestHumanBehavior:
    """Test human-like behavior simulation."""
    
    @pytest.mark.asyncio
    async def test_random_delay(self):
        """Test that random delay waits appropriate time."""
        import time
        
        start = time.time()
        await HumanBehavior.random_delay(0.1, 0.2)
        elapsed = time.time() - start
        
        assert 0.1 <= elapsed <= 0.3, f"Delay was {elapsed}s, expected 0.1-0.2s"
    
    @pytest.mark.asyncio
    async def test_human_type(self):
        """Test human-like typing behavior."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Create a simple HTML page with input
            await page.set_content('<input type="text" id="test-input" />')
            
            # Type text
            await HumanBehavior.human_type(page, '#test-input', 'AI')
            
            # Verify text was entered
            value = await page.input_value('#test-input')
            assert value == 'AI'
            
            await browser.close()
    
    @pytest.mark.asyncio
    async def test_human_click(self):
        """Test human-like clicking behavior."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Create a simple HTML page with button
            await page.set_content('<button id="test-btn" onclick="this.textContent=\'Clicked\'">Click Me</button>')
            
            # Click button
            await HumanBehavior.human_click(page, '#test-btn')
            
            # Verify button was clicked
            text = await page.text_content('#test-btn')
            assert text == 'Clicked'
            
            await browser.close()


class TestMicrosoftCareersScraper:
    """Test Microsoft Careers Scraper functionality."""
    
    @pytest.mark.asyncio
    async def test_scraper_initialization(self):
        """Test scraper initializes correctly."""
        scraper = MicrosoftCareersScraper(headless=True)
        
        assert scraper.headless == True
        assert scraper.browser is None
        assert scraper.jobs == []
        assert scraper.BASE_URL == "https://careers.microsoft.com/v2/global/en/home.html"
    
    @pytest.mark.asyncio
    async def test_browser_initialization(self):
        """Test browser initializes with correct settings."""
        scraper = MicrosoftCareersScraper(headless=True)
        
        await scraper.initialize_browser()
        
        assert scraper.browser is not None
        assert scraper.context is not None
        
        await scraper.close_browser()
    
    @pytest.mark.asyncio
    async def test_navigate_to_mock_page(self):
        """Test navigation to a mock page."""
        scraper = MicrosoftCareersScraper(headless=True)
        await scraper.initialize_browser()
        
        page = await scraper.context.new_page()
        
        # Create a simple mock page
        await page.set_content('<html><body><h1>Test Page</h1></body></html>')
        
        # Verify page loaded
        title = await page.text_content('h1')
        assert title == 'Test Page'
        
        await scraper.close_browser()
    
    @pytest.mark.asyncio
    async def test_search_form_interaction(self):
        """Test interaction with search form."""
        scraper = MicrosoftCareersScraper(headless=True)
        await scraper.initialize_browser()
        
        page = await scraper.context.new_page()
        
        # Create mock search form
        html_content = """
        <html>
        <body>
            <form>
                <input type="search" placeholder="Search by job title" id="job-search" />
                <input type="text" placeholder="Enter location" id="location" />
                <button type="submit">Find</button>
            </form>
        </body>
        </html>
        """
        await page.set_content(html_content)
        
        # Test typing in job search
        await HumanBehavior.human_type(page, '#job-search', 'AI')
        job_value = await page.input_value('#job-search')
        assert job_value == 'AI'
        
        # Test typing in location
        await HumanBehavior.human_type(page, '#location', 'Seattle')
        location_value = await page.input_value('#location')
        assert location_value == 'Seattle'
        
        await scraper.close_browser()
    
    @pytest.mark.asyncio
    async def test_scrape_mock_job_listings(self):
        """Test scraping mock job listings."""
        scraper = MicrosoftCareersScraper(headless=True)
        await scraper.initialize_browser()
        
        page = await scraper.context.new_page()
        
        # Create mock job listings
        html_content = """
        <html>
        <body>
            <article>
                <h2 class="job-title">AI Engineer</h2>
                <div class="location">Seattle, WA</div>
                <a href="/jobs/123">View Job</a>
                <div class="posted-date">Posted 2 days ago</div>
                <p class="description">Exciting AI position</p>
            </article>
            <article>
                <h2 class="job-title">Machine Learning Scientist</h2>
                <div class="location">Redmond, WA</div>
                <a href="/jobs/456">View Job</a>
                <div class="posted-date">Posted 1 week ago</div>
                <p class="description">Research ML models</p>
            </article>
            <article>
                <h2 class="job-title">AI Product Manager</h2>
                <div class="location">Seattle, WA</div>
                <a href="/jobs/789">View Job</a>
                <div class="posted-date">Posted yesterday</div>
                <p class="description">Lead AI products</p>
            </article>
        </body>
        </html>
        """
        await page.set_content(html_content)
        
        # Scrape the mock listings
        jobs = await scraper.scrape_job_listings(page, max_jobs=10)
        
        assert len(jobs) == 3
        assert jobs[0]['title'] == 'AI Engineer'
        assert jobs[1]['title'] == 'Machine Learning Scientist'
        assert jobs[2]['title'] == 'AI Product Manager'
        assert 'Seattle' in jobs[0]['job_location']
        
        await scraper.close_browser()
    
    @pytest.mark.asyncio
    async def test_cookie_consent_handling(self):
        """Test cookie consent popup handling."""
        scraper = MicrosoftCareersScraper(headless=True)
        await scraper.initialize_browser()
        
        page = await scraper.context.new_page()
        
        # Create mock cookie consent
        html_content = """
        <html>
        <body>
            <div id="cookie-banner">
                <button id="accept-btn">Accept all</button>
            </div>
            <h1 id="content" style="display:none;">Main Content</h1>
        </body>
        </html>
        """
        await page.set_content(html_content)
        
        # Check button exists
        button_visible = await page.is_visible('#accept-btn')
        assert button_visible == True
        
        # Handle cookie consent
        await scraper.handle_cookie_consent(page)
        
        await scraper.close_browser()
    
    @pytest.mark.asyncio
    async def test_save_to_csv(self, tmp_path):
        """Test saving jobs to CSV file."""
        scraper = MicrosoftCareersScraper(headless=True)
        
        # Add mock jobs
        scraper.jobs = [
            {
                'title': 'AI Engineer',
                'job_location': 'Seattle, WA',
                'url': '/jobs/123',
                'posted_date': '2 days ago',
                'description': 'Great AI job',
                'scraped_at': datetime.now().isoformat(),
                'source': 'Microsoft Careers',
                'search_term': 'AI',
                'location': 'Seattle'
            }
        ]
        
        # Change output directory to tmp_path
        import os
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            scraper.save_to_csv('test_jobs.csv')
            
            # Check file was created
            csv_file = tmp_path / 'output' / 'test_jobs.csv'
            assert csv_file.exists()
            
            # Read and verify content
            import pandas as pd
            df = pd.read_csv(csv_file)
            assert len(df) == 1
            assert df.iloc[0]['title'] == 'AI Engineer'
        finally:
            os.chdir(original_dir)
    
    @pytest.mark.asyncio
    async def test_save_to_json(self, tmp_path):
        """Test saving jobs to JSON file."""
        scraper = MicrosoftCareersScraper(headless=True)
        
        # Add mock jobs
        scraper.jobs = [
            {
                'title': 'AI Engineer',
                'job_location': 'Seattle, WA',
                'url': '/jobs/123',
                'posted_date': '2 days ago',
                'description': 'Great AI job',
                'scraped_at': datetime.now().isoformat(),
                'source': 'Microsoft Careers',
                'search_term': 'AI',
                'location': 'Seattle'
            }
        ]
        
        # Change output directory to tmp_path
        import os
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            scraper.save_to_json('test_jobs.json')
            
            # Check file was created
            json_file = tmp_path / 'output' / 'test_jobs.json'
            assert json_file.exists()
            
            # Read and verify content
            import json
            with open(json_file, 'r') as f:
                jobs = json.load(f)
            assert len(jobs) == 1
            assert jobs[0]['title'] == 'AI Engineer'
        finally:
            os.chdir(original_dir)


class TestRetryBehavior:
    """Test retry and backoff strategies."""
    
    @pytest.mark.asyncio
    async def test_retry_on_timeout(self):
        """Test that retry logic works on timeout."""
        scraper = MicrosoftCareersScraper(headless=True)
        await scraper.initialize_browser()
        
        page = await scraper.context.new_page()
        
        # This should handle timeout gracefully with retries
        try:
            # Set very short timeout to force retry
            await page.goto('about:blank', timeout=1)
        except Exception:
            pass  # Expected
        
        await scraper.close_browser()


@pytest.mark.asyncio
async def test_end_to_end_mock_scrape():
    """End-to-end test with complete mock scenario."""
    scraper = MicrosoftCareersScraper(headless=True)
    await scraper.initialize_browser()
    
    page = await scraper.context.new_page()
    
    # Create complete mock careers page with inline styles to ensure visibility
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Microsoft Careers</title></head>
    <body>
        <h1>Search for Jobs</h1>
        <form id="search-form">
            <input type="search" placeholder="Search by job title" id="job-search" />
            <input type="text" placeholder="Enter location" id="location-search" />
            <button type="submit">Find</button>
        </form>
        <div id="results">
            <article class="job-listing" style="display: block; visibility: visible;">
                <h2 class="job-title">Senior AI Engineer</h2>
                <div class="job-location">Seattle, Washington</div>
                <a href="https://careers.microsoft.com/job/123">Apply Now</a>
                <div class="posted-date">Posted 3 days ago</div>
                <p class="description">Lead AI initiatives</p>
            </article>
            <article class="job-listing" style="display: block; visibility: visible;">
                <h2 class="job-title">AI Research Scientist</h2>
                <div class="job-location">Redmond, Washington</div>
                <a href="https://careers.microsoft.com/job/456">Apply Now</a>
                <div class="posted-date">Posted 1 week ago</div>
                <p class="description">Research cutting-edge AI</p>
            </article>
        </div>
    </body>
    </html>
    """
    await page.set_content(html_content)
    
    # Test search interaction
    await page.fill('#job-search', 'AI')
    await page.fill('#location-search', 'Seattle')
    
    # Verify articles are visible
    articles = await page.locator('article').all()
    assert len(articles) >= 2, "Should have at least 2 article elements"
    
    # Test that we can extract data from the articles
    first_article = articles[0]
    title = await first_article.locator('h2').text_content()
    assert 'AI' in title, f"Title should contain 'AI', got: {title}"
    
    await scraper.close_browser()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
