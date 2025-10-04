# Search Box Selector Fix 🎯

## Issue
The search box on Microsoft Careers page wasn't being filled because the scraper was looking for generic selectors that didn't match the actual page structure.

**Actual Search Box HTML:**
```html
<input id="search-box9" 
       autocomplete="none" 
       class="ms-SearchBox-field field-542" 
       placeholder="Search by job title, ID, or keyword" 
       role="searchbox" 
       aria-label="Search by job title, ID, or keyword" 
       value="">
```

## Solution

Updated the selector priority list to target the actual Microsoft Careers search box:

### New Selector Priority (in order):
1. `#search-box9` - **Specific ID from Microsoft Careers page**
2. `input.ms-SearchBox-field` - **Class name from the page**
3. `input[placeholder*="keyword"]` - Matches the placeholder text
4. `input[placeholder*="job title"]` - Generic job title placeholder
5. `input[aria-label*="job title"]` - Aria label fallback
6. `input[aria-label*="keyword"]` - Aria label with keyword
7. `input[role="searchbox"]` - Role attribute
8. `input[type="search"]` - Generic search input
9. `#keyword` - Generic ID fallback

### Additional Improvements

1. **Field Clearing**: Added `await page.fill(selector, '')` to clear any existing values before typing
2. **Better Logging**: Added debug logging for failed selectors
3. **Wait Selector Update**: Updated initial wait to include the specific selectors

## Changes Made

### Files Modified
- ✅ `microsoft_scraper.py` - Updated `search_jobs()` method with new selectors
- ✅ `config.py` - Updated `SELECTORS['job_title_input']` configuration

### Code Changes

**Before:**
```python
job_title_selectors = [
    'input[placeholder*="job title"]',
    'input[aria-label*="job title"]',
    'input[placeholder*="keyword"]',
    'input[type="search"]',
    '#keyword',
]
```

**After:**
```python
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
```

## Testing

✅ All 13 tests passing

## What to Expect Now

When you run the scraper, you should see:

```
INFO - Searching for 'AI' jobs in 'Seattle'
INFO - Found job title field: #search-box9
INFO - Found location field: [location selector]
INFO - Found search button: [button selector]
INFO - Search completed successfully
```

The search box will now be properly filled with your search term!

## Try It Now

```bash
source .venv/bin/activate
python run_scraper.py
```

Watch the browser:
- ✅ Search box gets filled with "AI"
- ✅ Location field gets filled (if available)
- ✅ Search button is clicked
- ✅ Results page loads
- ✅ Jobs are scraped

## Troubleshooting

If the search box still doesn't fill:

1. **Check the browser console** - Look for JavaScript errors
2. **Verify the selector** - The ID might have changed (e.g., `search-box10`)
3. **Try waiting longer** - Increase the initial delay:
   ```python
   await HumanBehavior.random_delay(2, 4)
   ```
4. **Inspect the page** - Right-click the search box and check its ID/class

### How to Find New Selectors

If Microsoft changes the page structure:

1. Open the page in Chrome
2. Right-click the search box → Inspect
3. Look for:
   - `id` attribute (most reliable)
   - `class` attribute (may have multiple)
   - `placeholder` text
   - `aria-label` text
4. Update the selector list in `microsoft_scraper.py`

## Technical Notes

- **Selector Order Matters**: More specific selectors are tried first
- **Fallback Strategy**: If one selector fails, the next is tried
- **Field Clearing**: Ensures no old values interfere with typing
- **Robust Error Handling**: Continues to next selector on failure

---

**Fixed on:** October 3, 2025  
**Tested on:** Microsoft Careers with search box ID `search-box9`  
**Status:** ✅ Working
