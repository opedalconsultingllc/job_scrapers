# Location Field & Job Listings Fix 🎯

## Issues Identified

### Problem 1: Location Field Not Filling
The location input field wasn't being found/filled with the generic selectors.

### Problem 2: No Jobs Scraped (1700+ results returned but 0 captured)
The job listing container selectors weren't matching the actual Microsoft Careers page structure. Modern web apps often use:
- React/Fabric UI components with specific class names
- `role="listitem"` instead of `article` tags
- Dynamic class names with prefixes

## Solutions Implemented

### 1. Enhanced Location Field Selectors

**Updated selectors priority:**
```python
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
```

**Improvements:**
- ✅ Added field clearing before typing
- ✅ Added debug logging for failed selectors
- ✅ More specific ID patterns

### 2. Comprehensive Job Listings Selectors

**Major Update:** Added modern React/Fabric UI selectors:

```python
listing_selectors = [
    '[role="listitem"]',  # ⭐ Common in modern React apps
    '[data-job-id]',
    '[data-automation*="job"]',
    'article',
    'ul[role="list"] > li',  # ⭐ List structure
    '.ms-List-cell',  # ⭐ Microsoft Fabric UI
    '[class*="jobCard"]',
    '[class*="job-card"]',
    '[class*="JobCard"]',
    '.job-listing',
    '.job-item',
    '[class*="searchResult"]',
    '[class*="result-item"]',
]
```

**Key additions:**
- `[role="listitem"]` - Most likely match for modern Microsoft pages
- `.ms-List-cell` - Microsoft Fabric UI component
- `[data-automation*="job"]` - Test automation attributes
- Class name wildcards for variations

### 3. Enhanced Data Extraction

**Multi-Selector Approach:** Each field now tries multiple selectors until one works:

#### Title Extraction
```python
title_selectors = [
    'h2', 'h3', 'h4',
    '[class*="title"]', '[class*="Title"]',
    '[data-automation*="title"]',
    'a[class*="title"]',
    '.ms-Link'
]
```

#### Location Extraction
```python
location_selectors = [
    '[class*="location"]', '[class*="Location"]',
    '[aria-label*="location"]',
    '[data-automation*="location"]',
    'span[class*="city"]',
    'div[class*="city"]'
]
```

#### URL Extraction
- Tries to get `href` from links
- Makes relative URLs absolute
- Falls back to `data-job-id` attribute
- Constructs URL from job ID if available

#### Date Extraction
```python
date_selectors = [
    '[class*="date"]', '[class*="Date"]',
    '[class*="posted"]', '[class*="Posted"]',
    '[data-automation*="date"]',
    'time'
]
```

#### Description Extraction
- Tries specific description selectors
- Falls back to all element text if no description found
- Limits to first 500 characters for fallback

### 4. Improved Error Handling & Debugging

**Added diagnostic logging:**
```python
# If no jobs found, log page state
if not job_elements:
    page_text = await page.evaluate("() => document.body.innerText")
    logger.error("No job listings found with any selector!")
    logger.info(f"Page text preview: {page_text[:500]}")
    logger.info(f"Current URL: {page.url}")
```

**Wait strategy:**
- Tries multiple wait selectors
- Logs which selector succeeded
- Continues even if wait times out (graceful degradation)

### 5. Updated Configuration File

`config.py` now includes all new selectors organized by purpose:
- `job_title_input` - 9 selectors
- `location_input` - 8 selectors (NEW)
- `search_button` - 7 selectors
- `job_listings` - 13 selectors (EXPANDED)
- `job_title` - 7 selectors (NEW)
- `job_location` - 6 selectors (NEW)
- `job_date` - 6 selectors (NEW)

## Files Modified

✅ `microsoft_scraper.py`
- Enhanced `search_jobs()` method with location field improvements
- Completely rewrote `scrape_job_listings()` method
- Added comprehensive selector fallbacks
- Improved error handling and debugging

✅ `config.py`
- Added all new selector configurations
- Organized by component type
- Documented selector purposes

## Testing

✅ All 13 tests passing

## What Changed - Quick Summary

### Before:
```python
# Limited selectors
listing_selectors = [
    'article',
    '.job-listing',
    '.job-item',
]

# Simple extraction
title = await element.locator('h2, h3, .job-title').first.text_content()
```

### After:
```python
# Comprehensive selectors
listing_selectors = [
    '[role="listitem"]',  # Modern React
    '[data-job-id]',
    'ul[role="list"] > li',
    '.ms-List-cell',  # Microsoft Fabric UI
    ... # 9 more options
]

# Robust extraction with fallbacks
for title_sel in title_selectors:
    try:
        title_elem = element.locator(title_sel).first
        title_text = await title_elem.text_content()
        if title_text and title_text.strip():
            job_data['title'] = title_text.strip()
            break
    except:
        continue
```

## Expected Behavior Now

When you run the scraper, you should see:

```
INFO - Searching for 'AI' jobs in 'Seattle'
INFO - Found job title field: #search-box9
INFO - Found location field: input#location-box9  # ✅ NOW WORKS
INFO - Search completed successfully
INFO - Waiting for job listings to appear...
INFO - Found elements with selector: [role="listitem"]  # ✅ NEW
INFO - Found 1700 job listings with selector: [role="listitem"]  # ✅ NOW CAPTURES
INFO - Scraped job 1/50: Senior AI Engineer
INFO - Scraped job 2/50: Machine Learning Specialist
...
INFO - Successfully scraped 50 jobs
```

## Try It Now

```bash
source .venv/bin/activate
python run_scraper.py
```

## Troubleshooting

### If location field still doesn't fill:
1. Run the `quick_inspect.py` script to see actual field IDs
2. Look for the location input in browser dev tools
3. Add the specific ID/class to the top of `location_selectors`

### If jobs still aren't captured:
1. Check the logs for "Found X job listings with selector: Y"
2. If no selector works, run `quick_inspect.py` to capture actual structure
3. Look in `page_inspection_results.json` for the actual container classes
4. Add those selectors to `listing_selectors`

### Diagnostic Commands

```bash
# Run the page inspector
python quick_inspect.py

# Check the results
cat page_inspection_results.json | python -m json.tool

# Run scraper with verbose logging
python run_scraper.py --quick
```

## Manual Inspection Method

If automated inspection fails:

1. Open browser:
   ```bash
   python run_scraper.py
   ```

2. Let it navigate to results page

3. In browser dev tools (Right-click → Inspect):
   - Find a job listing element
   - Look for:
     - Container element (likely has `role="listitem"` or `class*="job"`)
     - Title element (look for h2, h3, or `class*="title"`)
     - Location element (look for `class*="location"`)

4. Update selectors in `microsoft_scraper.py` if needed

## Key Improvements Summary

1. ✅ **Location field** - 8 comprehensive selectors
2. ✅ **Job listings** - 13 selectors including modern React patterns
3. ✅ **Data extraction** - Multiple fallbacks for each field
4. ✅ **Error handling** - Detailed logging for debugging
5. ✅ **URL handling** - Converts relative URLs to absolute
6. ✅ **Graceful degradation** - Continues even if some fields missing

---

**Updated on:** October 3, 2025  
**Tested on:** All tests passing (13/13)  
**Status:** ✅ Ready to test on live site
