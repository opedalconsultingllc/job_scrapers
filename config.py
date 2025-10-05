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
        '#search-box9',  # Specific ID from Microsoft Careers
        'input.ms-SearchBox-field',  # Class name from the actual page
        'input[placeholder*="keyword"]',
        'input[placeholder*="job title"]',
        'input[aria-label*="job title"]',
        'input[aria-label*="keyword"]',
        'input[role="searchbox"]',
        'input[type="search"]',
        '#keyword',
    ],
    'location_input': [
        'input#location-box9',  # Specific ID pattern (matching search-box9)
        'input[id*="location"]',  # Any input with 'location' in ID
        'input[placeholder*="location"]',
        'input[aria-label*="location"]',
        'input[placeholder*="city"]',
        'input[placeholder*="where"]',
        'input[name*="location"]',
        '#location',
    ],
    'search_button': [
        'button:has-text("Find")',
        'button:has-text("Search")',
        'button[type="submit"]',
        'input[type="submit"]',
        '.search-button',
        'button[aria-label*="search"]',
        'button[aria-label*="find"]',
    ],
    'job_listings': [
        'div.ms-List-cell[role="listitem"]',  # ⭐ ACTUAL from Microsoft Careers
        '[role="listitem"].ms-List-cell',  # Alternative format
        '.ms-List-cell',  # Microsoft Fabric UI
        '[role="listitem"]',  # Common in modern React apps
        '[data-job-id]',
        '[data-automation*="job"]',
        'article',
        'ul[role="list"] > li',
        '[class*="jobCard"]',
        '[class*="job-card"]',
        '[class*="JobCard"]',
        '.job-listing',
        '.job-item',
        '[class*="searchResult"]',
        '[class*="result-item"]',
    ],
    'job_title': [
        'h2.MZGzlrn8gfgSs8TZHhv2',  # ⭐ ACTUAL from Microsoft Careers
        'h2', 'h3', 'h4',
        '[class*="title"]',
        '[class*="Title"]',
        '[data-automation*="title"]',
        'a[class*="title"]',
        '.ms-Link',
    ],
    'job_location': [
        'i[data-icon-name="POI"] + span',  # ⭐ ACTUAL: span after location icon
        'i.wwxC8vs2c2O5YaFddx7C + span',  # Alternative with class
        '[class*="location"]',
        '[class*="Location"]',
        '[aria-label*="location"]',
        '[data-automation*="location"]',
        'span[class*="city"]',
        'div[class*="city"]',
    ],
    'job_date': [
        'i[data-icon-name="Clock"] + span',  # ⭐ ACTUAL: span after clock icon
        '[class*="date"]',
        '[class*="Date"]',
        '[class*="posted"]',
        '[class*="Posted"]',
        '[data-automation*="date"]',
        'time',
    ],
    'job_description': [
        'span[aria-label="job description"]',  # ⭐ ACTUAL from inspection
        'span.css-544',  # Alternative with class
        'p',
        '[class*="description"]',
        '[class*="Description"]',
        '[class*="snippet"]',
        '[data-automation*="description"]',
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
