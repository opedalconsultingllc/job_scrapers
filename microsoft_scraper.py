"""
Microsoft Careers Scraper
Scrapes AI job listings from Microsoft Careers website using Playwright
with human-like behavior and backoff strategies.
"""

import asyncio
import random
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import pandas as pd


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HumanBehavior:
    """Simulates human-like behavior for web scraping."""
    
    @staticmethod
    async def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add random delay to simulate human reading time."""
        delay = random.uniform(min_seconds, max_seconds)
        logger.debug(f"Waiting {delay:.2f} seconds")
        await asyncio.sleep(delay)
    
    @staticmethod
    async def human_type(page: Page, selector: str, text: str):
        """Type text character by character with random delays."""
        await page.click(selector)
        await HumanBehavior.random_delay(0.3, 0.8)
        
        for char in text:
            await page.type(selector, char)
            await asyncio.sleep(random.uniform(0.05, 0.15))
        
        await HumanBehavior.random_delay(0.5, 1.0)
    
    @staticmethod
    async def human_click(page: Page, selector: str):
        """Click with human-like delay."""
        await HumanBehavior.random_delay(0.5, 1.5)
        await page.click(selector)
        await HumanBehavior.random_delay(1.0, 2.0)
    
    @staticmethod
    async def random_mouse_movement(page: Page):
        """Simulate random mouse movements."""
        viewport = page.viewport_size
        if viewport:
            x = random.randint(0, viewport['width'])
            y = random.randint(0, viewport['height'])
            await page.mouse.move(x, y)
            await HumanBehavior.random_delay(0.2, 0.5)


class MicrosoftCareersScraper:
    """Scraper for Microsoft Careers website."""
    
    BASE_URL = "https://careers.microsoft.com/v2/global/en/home.html"
    
    def __init__(self, headless: bool = False):
        """
        Initialize the scraper.
        
        Args:
            headless: Whether to run browser in headless mode (default: False)
        """
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.jobs: List[Dict] = []
    
    async def initialize_browser(self):
        """Initialize Playwright browser with human-like settings."""
        self.playwright = await async_playwright().start()
        
        # Launch browser with realistic viewport and user agent
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-notifications',  # Disable notification prompts
                '--disable-popup-blocking',
                '--disable-infobars',
            ]
        )
        
        # Create context with realistic settings and block notifications
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/Los_Angeles',
            permissions=[],  # Don't grant any permissions
            ignore_https_errors=True,
        )
        
        # Additional anti-detection measures
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        logger.info("Browser initialized successfully")
    
    async def setup_dialog_handlers(self, page: Page):
        """Set up handlers to automatically dismiss dialogs and pop-ups."""
        async def handle_dialog(dialog):
            logger.info(f"Dialog detected: {dialog.type} - {dialog.message}")
            try:
                await dialog.dismiss()
                logger.info("Dialog dismissed")
            except Exception as e:
                logger.warning(f"Error dismissing dialog: {e}")
        
        # Register dialog handler
        page.on("dialog", handle_dialog)
        logger.info("Dialog handlers registered")
    
    async def close_browser(self):
        """Close browser and cleanup resources."""
        if self.browser:
            await self.browser.close()
            await self.playwright.stop()
            logger.info("Browser closed")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=30),
        retry=retry_if_exception_type(PlaywrightTimeout),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def navigate_to_homepage(self, page: Page) -> bool:
        """
        Navigate to Microsoft Careers homepage with retry logic.
        
        Args:
            page: Playwright page object
            
        Returns:
            bool: True if navigation successful
        """
        logger.info(f"Navigating to {self.BASE_URL}")
        
        try:
            await page.goto(self.BASE_URL, wait_until='networkidle', timeout=30000)
            await HumanBehavior.random_delay(2, 4)
            
            # Wait for page to be interactive
            await page.wait_for_load_state('domcontentloaded')
            
            logger.info("Successfully loaded homepage")
            return True
            
        except PlaywrightTimeout:
            logger.error("Timeout loading homepage")
            raise
        except Exception as e:
            logger.error(f"Error navigating to homepage: {e}")
            return False
    
    async def handle_cookie_consent(self, page: Page):
        """Handle cookie consent popup if present."""
        try:
            # Look for common cookie consent selectors
            cookie_selectors = [
                'button:has-text("Accept")',
                'button:has-text("Accept all")',
                'button:has-text("I agree")',
                '#cookie-banner button',
            ]
            
            for selector in cookie_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        await HumanBehavior.human_click(page, selector)
                        logger.info("Cookie consent accepted")
                        return
                except Exception:
                    continue
                    
        except Exception as e:
            logger.debug(f"No cookie consent found or error handling it: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=30),
        retry=retry_if_exception_type(Exception),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def search_jobs(self, page: Page, job_title: str = "AI", location: str = "Seattle") -> bool:
        """
        Search for jobs with given criteria.
        
        Args:
            page: Playwright page object
            job_title: Job title to search for
            location: Location to search in
            
        Returns:
            bool: True if search successful
        """
        logger.info(f"Searching for '{job_title}' jobs in '{location}'")
        
        try:
            # Wait for search form to be visible with more specific selectors
            await page.wait_for_selector('#search-box9, input[placeholder*="job title"], input[aria-label*="job title"], .ms-SearchBox-field', timeout=15000)
            await HumanBehavior.random_delay(1, 2)
            
            # Find and fill job title field - prioritize the actual ID from the page
            job_title_selectors = [
                '#search-box9',  # Specific ID from Microsoft Careers
                'input.ms-SearchBox-field',  # Class name from the actual page
                'input[placeholder*="keyword"]',
                'input[placeholder*="job title"]',
                'input[aria-label*="job title"]',
                'input[aria-label*="keyword"]',
                'input[role="searchbox"]',
                'input[type="search"]',
                '#keyword',
            ]
            
            job_field_found = False
            for selector in job_title_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        logger.info(f"Found job title field: {selector}")
                        # Clear any existing value first
                        await page.fill(selector, '')
                        await HumanBehavior.random_delay(0.3, 0.8)
                        # Type the search term
                        await HumanBehavior.human_type(page, selector, job_title)
                        job_field_found = True
                        break
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            if not job_field_found:
                logger.error("Could not find job title input field")
                return False
            
            # Find and fill location field
            location_selectors = [
                'input#location-box9',  # Specific ID pattern (matching search-box9 pattern)
                'input[id*="location"]',  # Any input with 'location' in ID
                'input[placeholder*="location"]',
                'input[aria-label*="location"]',
                'input[placeholder*="city"]',
                'input[placeholder*="where"]',
                'input[name*="location"]',
                '#location',
            ]
            
            location_field_found = False
            for selector in location_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        logger.info(f"Found location field: {selector}")
                        # Clear and fill location field
                        await page.fill(selector, '')
                        await HumanBehavior.random_delay(0.3, 0.8)
                        await HumanBehavior.human_type(page, selector, location)
                        location_field_found = True
                        await HumanBehavior.random_delay(1, 2)
                        break
                except Exception as e:
                    logger.debug(f"Location selector {selector} failed: {e}")
                    continue
            
            if not location_field_found:
                logger.warning("Could not find location input field, continuing anyway")
            
            # Click search/find button
            search_button_selectors = [
                'button:has-text("Find")',
                'button:has-text("Search")',
                'button[type="submit"]',
                'input[type="submit"]',
                '.search-button',
            ]
            
            button_found = False
            for selector in search_button_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        logger.info(f"Found search button: {selector}")
                        await HumanBehavior.human_click(page, selector)
                        button_found = True
                        break
                except Exception:
                    continue
            
            if not button_found:
                # Try pressing Enter as fallback
                logger.info("Search button not found, trying Enter key")
                await page.keyboard.press('Enter')
            
            # Wait for results to load
            await page.wait_for_load_state('networkidle', timeout=20000)
            await HumanBehavior.random_delay(2, 4)
            
            logger.info("Search completed successfully")
            return True
            
        except PlaywrightTimeout:
            logger.error("Timeout during job search")
            raise
        except Exception as e:
            logger.error(f"Error searching for jobs: {e}")
            raise
    
    async def scrape_job_listings(self, page: Page, max_jobs: int = 50) -> List[Dict]:
        """
        Scrape job listings from search results.
        
        Args:
            page: Playwright page object
            max_jobs: Maximum number of jobs to scrape
            
        Returns:
            List of job dictionaries
        """
        logger.info(f"Scraping job listings (max: {max_jobs})")
        jobs = []
        
        try:
            # Wait for job listings to appear - try multiple possible selectors
            logger.info("Waiting for job listings to appear...")
            
            # First, wait for results indicator
            try:
                await page.wait_for_selector('h1:has-text("results"), h1:has-text("result")', timeout=10000)
                logger.info("Results counter found - jobs should be present")
                await HumanBehavior.random_delay(2, 3)  # Extra wait for dynamic content
            except Exception:
                logger.warning("Results counter not found, continuing anyway")
            
            # Try to wait for any of these selectors
            wait_selectors = [
                'article',
                '[role="listitem"]',
                '[data-job-id]',
                '[class*="job"]',
                'ul[role="list"] > li',
                '.ms-List-cell',
                'a[href*="/job"]',  # Links containing /job
                'div[class*="card"]',
                'div[class*="result"]'
            ]
            
            waited = False
            for wait_sel in wait_selectors:
                try:
                    await page.wait_for_selector(wait_sel, timeout=10000)
                    logger.info(f"Found elements with selector: {wait_sel}")
                    waited = True
                    break
                except Exception:
                    continue
            
            if not waited:
                logger.warning("Could not find any expected job listing elements")
                # Log page structure for debugging
                html_snippet = await page.evaluate("() => document.body.innerHTML.substring(0, 2000)")
                logger.debug(f"Page HTML preview: {html_snippet}")
            
            await HumanBehavior.random_delay(2, 3)
            
            # Try comprehensive list of selectors for job listings
            listing_selectors = [
                '[role="listitem"]',  # Common in modern React apps
                '[data-job-id]',
                '[data-automation*="job"]',
                'article',
                'ul[role="list"] > li',
                '.ms-List-cell',  # Microsoft Fabric UI
                '[class*="jobCard"]',
                '[class*="job-card"]',
                '[class*="JobCard"]',
                '.job-listing',
                '.job-item',
                '[class*="searchResult"]',
                '[class*="result-item"]',
                'div[class*="job"]',  # Any div with 'job' in class
                'div[class*="card"]',  # Card-based layouts
                'a[href*="/job/"]',  # Links with /job/ in URL
            ]
            
            job_elements = None
            used_selector = None
            
            for selector in listing_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if len(elements) > 0:
                        logger.info(f"Found {len(elements)} elements with selector: {selector}")
                        
                        # Verify these are actually job elements by checking content
                        # A job element should have substantial text content
                        valid_elements = []
                        for elem in elements[:10]:  # Check first 10
                            try:
                                text = await elem.text_content()
                                if text and len(text.strip()) > 30:  # At least 30 chars
                                    valid_elements.append(elem)
                            except:
                                continue
                        
                        if valid_elements:
                            logger.info(f"Verified {len(valid_elements)} valid job elements")
                            job_elements = elements  # Use all elements if some are valid
                            used_selector = selector
                            break
                        else:
                            logger.debug(f"Elements found with {selector} don't look like jobs")
                            
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            if not job_elements:
                # Last resort: try to find job elements by looking for patterns
                logger.warning("Standard selectors failed, trying pattern-based search...")
                
                try:
                    # Look for elements that have links with job URLs
                    job_elements = await page.locator('a[href*="/job/"]').all()
                    if job_elements:
                        # Get parent elements as those are likely the job containers
                        parent_elements = []
                        for link in job_elements[:50]:  # Limit to first 50
                            try:
                                parent = await link.evaluate_handle("el => el.closest('li, div, article')")
                                if parent:
                                    parent_elements.append(parent)
                            except:
                                continue
                        
                        if parent_elements:
                            job_elements = parent_elements
                            used_selector = "parent of a[href*='/job/']"
                            logger.info(f"Found {len(job_elements)} job elements via parent search")
                except Exception as e:
                    logger.error(f"Pattern-based search failed: {e}")
            
            if not job_elements:
                # Last resort: log page content for debugging
                page_text = await page.evaluate("() => document.body.innerText")
                logger.error("No job listings found with any selector!")
                logger.info(f"Page text preview: {page_text[:500]}")
                logger.info(f"Current URL: {page.url}")
                
                # Try to get page structure
                structure = await page.evaluate("""
                    () => {
                        const allElements = {};
                        ['article', 'li', 'div', 'a'].forEach(tag => {
                            allElements[tag] = document.querySelectorAll(tag).length;
                        });
                        return allElements;
                    }
                """)
                logger.info(f"Page structure: {structure}")
                return jobs
            
            # Limit to max_jobs
            job_elements = job_elements[:max_jobs]
            logger.info(f"Processing {len(job_elements)} job elements (using selector: {used_selector})")
            
            # Extract job information
            for idx, element in enumerate(job_elements, 1):
                try:
                    await HumanBehavior.random_delay(0.5, 1.5)
                    
                    # Extract job details
                    job_data = {
                        'scraped_at': datetime.now().isoformat(),
                        'source': 'Microsoft Careers',
                        'search_term': 'AI',
                        'location': 'Seattle',
                    }
                    
                    # Try to extract title with multiple selectors
                    try:
                        title_selectors = [
                            'h2', 'h3', 'h4',
                            '[class*="title"]', '[class*="Title"]',
                            '[data-automation*="title"]',
                            'a[class*="title"]',
                            '.ms-Link'
                        ]
                        title_found = False
                        for title_sel in title_selectors:
                            try:
                                title_elem = element.locator(title_sel).first
                                title_text = await title_elem.text_content()
                                if title_text and title_text.strip():
                                    job_data['title'] = title_text.strip()
                                    title_found = True
                                    break
                            except:
                                continue
                        if not title_found:
                            job_data['title'] = 'N/A'
                    except Exception:
                        job_data['title'] = 'N/A'
                    
                    # Try to extract location with multiple selectors
                    try:
                        location_selectors = [
                            '[class*="location"]', '[class*="Location"]',
                            '[aria-label*="location"]',
                            '[data-automation*="location"]',
                            'span[class*="city"]',
                            'div[class*="city"]'
                        ]
                        location_found = False
                        for loc_sel in location_selectors:
                            try:
                                location_elem = element.locator(loc_sel).first
                                location_text = await location_elem.text_content()
                                if location_text and location_text.strip():
                                    job_data['job_location'] = location_text.strip()
                                    location_found = True
                                    break
                            except:
                                continue
                        if not location_found:
                            job_data['job_location'] = 'N/A'
                    except Exception:
                        job_data['job_location'] = 'N/A'
                    
                    # Try to extract job ID or URL
                    try:
                        # First try to get href from any link in the element
                        link_elem = element.locator('a').first
                        href = await link_elem.get_attribute('href')
                        if href:
                            # Make it absolute if relative
                            if href.startswith('/'):
                                job_data['url'] = f"https://careers.microsoft.com{href}"
                            else:
                                job_data['url'] = href
                        else:
                            job_data['url'] = 'N/A'
                    except Exception:
                        # Try to get data-job-id or similar
                        try:
                            job_id = await element.get_attribute('data-job-id')
                            if job_id:
                                job_data['url'] = f"https://careers.microsoft.com/job/{job_id}"
                            else:
                                job_data['url'] = 'N/A'
                        except:
                            job_data['url'] = 'N/A'
                    
                    # Try to extract posting date
                    try:
                        date_selectors = [
                            '[class*="date"]', '[class*="Date"]',
                            '[class*="posted"]', '[class*="Posted"]',
                            '[data-automation*="date"]',
                            'time'
                        ]
                        date_found = False
                        for date_sel in date_selectors:
                            try:
                                date_elem = element.locator(date_sel).first
                                date_text = await date_elem.text_content()
                                if date_text and date_text.strip():
                                    job_data['posted_date'] = date_text.strip()
                                    date_found = True
                                    break
                            except:
                                continue
                        if not date_found:
                            job_data['posted_date'] = 'N/A'
                    except Exception:
                        job_data['posted_date'] = 'N/A'
                    
                    # Try to extract description snippet
                    try:
                        desc_selectors = [
                            'p', '[class*="description"]', '[class*="Description"]',
                            '[class*="snippet"]', '[data-automation*="description"]'
                        ]
                        desc_found = False
                        for desc_sel in desc_selectors:
                            try:
                                desc_elem = element.locator(desc_sel).first
                                desc_text = await desc_elem.text_content()
                                if desc_text and len(desc_text.strip()) > 20:  # Meaningful description
                                    job_data['description'] = desc_text.strip()
                                    desc_found = True
                                    break
                            except:
                                continue
                        if not desc_found:
                            # Fallback: get all text from element
                            all_text = await element.text_content()
                            if all_text:
                                job_data['description'] = all_text.strip()[:500]  # First 500 chars
                            else:
                                job_data['description'] = 'N/A'
                    except Exception:
                        job_data['description'] = 'N/A'
                    
                    jobs.append(job_data)
                    logger.info(f"Scraped job {idx}/{len(job_elements)}: {job_data['title']}")
                    
                except Exception as e:
                    logger.warning(f"Error scraping job {idx}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error scraping job listings: {e}")
            return jobs
    
    async def scrape(self, job_title: str = "AI", location: str = "Seattle", max_jobs: int = 50) -> List[Dict]:
        """
        Main scraping method.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            max_jobs: Maximum number of jobs to scrape
            
        Returns:
            List of job dictionaries
        """
        try:
            await self.initialize_browser()
            page = await self.context.new_page()
            
            # Set up dialog handlers
            await self.setup_dialog_handlers(page)
            
            # Navigate to homepage
            if not await self.navigate_to_homepage(page):
                return []
            
            # Handle cookie consent
            await self.handle_cookie_consent(page)
            
            # Perform search
            if not await self.search_jobs(page, job_title, location):
                return []
            
            # Scrape job listings
            self.jobs = await self.scrape_job_listings(page, max_jobs)
            
            return self.jobs
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return []
        finally:
            await self.close_browser()
    
    def save_to_csv(self, filename: Optional[str] = None):
        """Save scraped jobs to CSV file."""
        if not self.jobs:
            logger.warning("No jobs to save")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"microsoft_ai_jobs_{timestamp}.csv"
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        df = pd.DataFrame(self.jobs)
        df.to_csv(filepath, index=False)
        
        logger.info(f"Saved {len(self.jobs)} jobs to {filepath}")
    
    def save_to_json(self, filename: Optional[str] = None):
        """Save scraped jobs to JSON file."""
        import json
        
        if not self.jobs:
            logger.warning("No jobs to save")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"microsoft_ai_jobs_{timestamp}.json"
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.jobs)} jobs to {filepath}")


async def main():
    """Main execution function."""
    scraper = MicrosoftCareersScraper(headless=False)
    
    try:
        jobs = await scraper.scrape(
            job_title="AI",
            location="Seattle",
            max_jobs=50
        )
        
        if jobs:
            print(f"\n{'='*60}")
            print(f"Successfully scraped {len(jobs)} jobs!")
            print(f"{'='*60}\n")
            
            # Display first 3 jobs
            for idx, job in enumerate(jobs[:3], 1):
                print(f"Job {idx}:")
                print(f"  Title: {job.get('title', 'N/A')}")
                print(f"  Location: {job.get('job_location', 'N/A')}")
                print(f"  Posted: {job.get('posted_date', 'N/A')}")
                print(f"  URL: {job.get('url', 'N/A')[:80]}...")
                print()
            
            # Save results
            scraper.save_to_csv()
            scraper.save_to_json()
        else:
            print("No jobs were scraped")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
