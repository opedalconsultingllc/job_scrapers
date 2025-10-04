"""
Configuration file for Microsoft Careers Scraper
"""

# Scraper settings
SCRAPER_CONFIG = {
    'headless': False,  # Set to True for headless mode
    'default_job_title': 'AI',
    'default_location': 'Seattle',
    'max_jobs': 50,
}

# Browser settings
BROWSER_CONFIG = {
    'viewport': {
        'width': 1920,
        'height': 1080
    },
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'locale': 'en-US',
    'timezone_id': 'America/Los_Angeles',
}

# Timing settings (in seconds)
TIMING_CONFIG = {
    'min_delay': 1.0,
    'max_delay': 3.0,
    'typing_min_delay': 0.05,
    'typing_max_delay': 0.15,
    'click_delay_min': 0.5,
    'click_delay_max': 1.5,
    'page_load_timeout': 30000,  # milliseconds
    'element_timeout': 15000,  # milliseconds
}

# Retry settings
RETRY_CONFIG = {
    'max_attempts': 3,
    'backoff_multiplier': 2,
    'backoff_min': 4,
    'backoff_max': 30,
}

# Selectors for Microsoft Careers
SELECTORS = {
    'job_title_input': [
        'input[placeholder*="job title"]',
        'input[aria-label*="job title"]',
        'input[placeholder*="keyword"]',
        'input[type="search"]',
        '#keyword',
    ],
    'location_input': [
        'input[placeholder*="location"]',
        'input[aria-label*="location"]',
        'input[placeholder*="city"]',
        '#location',
    ],
    'search_button': [
        'button:has-text("Find")',
        'button:has-text("Search")',
        'button[type="submit"]',
        'input[type="submit"]',
        '.search-button',
    ],
    'job_listings': [
        'article',
        '.job-listing',
        '.job-item',
        '.job-card',
        '[data-job-id]',
        '[role="article"]',
    ],
    'cookie_consent': [
        'button:has-text("Accept")',
        'button:has-text("Accept all")',
        'button:has-text("I agree")',
        '#cookie-banner button',
    ],
}

# Output settings
OUTPUT_CONFIG = {
    'directory': 'output',
    'csv_prefix': 'microsoft_ai_jobs',
    'json_prefix': 'microsoft_ai_jobs',
    'timestamp_format': '%Y%m%d_%H%M%S',
}

# Logging settings
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
}
