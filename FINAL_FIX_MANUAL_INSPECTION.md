# FINAL FIX - Correct Selectors from Manual Inspection ✅

## The Solution

Based on your manual inspection of the Microsoft Careers page, I've updated the scraper with the **exact selectors** from the actual page structure.

## What You Found

### Job Container
```html
<div role="listitem" class="ms-List-cell" data-list-index="1">
  <!-- Job content here -->
</div>
```
**Selector:** `div.ms-List-cell[role="listitem"]`

### Job Title
```html
<h2 class="MZGzlrn8gfgSs8TZHhv2" style="margin: 3% 9% 5px 3%...">
  Machine Learning Engineer II
</h2>
```
**Selector:** `h2.MZGzlrn8gfgSs8TZHhv2`

### Location
```html
<i data-icon-name="POI" role="img" aria-label="job location icon"></i>
<span>Redmond, Washington, United States</span>
```
**Selector:** `i[data-icon-name="POI"] + span`

### Posted Date
```html
<i data-icon-name="Clock" role="img" aria-label="posted details icon"></i>
<span>1 day ago</span>
```
**Selector:** `i[data-icon-name="Clock"] + span`

### Description
```html
<span aria-label="job description" class="css-544">
  Viva Engage connects people through communities...
</span>
```
**Selector:** `span[aria-label="job description"]`

### Job ID
```html
<div aria-label="Job item 1827725" class="ms-Stack css-412">
```
**Extracted from:** `aria-label` attribute, then construct URL:
`https://careers.microsoft.com/us/en/job/1827725`

## Changes Made

### 1. Updated `microsoft_scraper.py`

**Container Selector (Line ~388):**
```python
listing_selectors = [
    'div.ms-List-cell[role="listitem"]',  # ⭐ ACTUAL from inspection
    '[role="listitem"].ms-List-cell',
    '.ms-List-cell',
    # ... fallbacks
]
```

**Title Extraction (Line ~545):**
```python
title_selectors = [
    'h2.MZGzlrn8gfgSs8TZHhv2',  # ⭐ ACTUAL class
    'h2',  # Fallback
    # ...
]
```

**Location Extraction (Line ~567):**
```python
location_selectors = [
    'i[data-icon-name="POI"] + span',  # ⭐ ACTUAL
    'i.wwxC8vs2c2O5YaFddx7C + span',
    # ... fallbacks
]
```

**Date Extraction (Line ~611):**
```python
date_selectors = [
    'i[data-icon-name="Clock"] + span',  # ⭐ ACTUAL
    # ... fallbacks
]
```

**Description Extraction (Line ~629):**
```python
desc_selectors = [
    'span[aria-label="job description"]',  # ⭐ ACTUAL
    'span.css-544',
    # ... fallbacks
]
```

**Job ID & URL (Line ~590):**
```python
# Extract job ID from aria-label "Job item XXXXX"
aria_label = await element.get_attribute('aria-label')
if aria_label and 'Job item' in aria_label:
    job_id = aria_label.replace('Job item ', '').strip()
    job_data['url'] = f"https://careers.microsoft.com/us/en/job/{job_id}"
    job_data['job_id'] = job_id
```

### 2. Updated `config.py`

All selectors in the config file now match the actual page structure with the specific selectors listed first.

## Test It Now! 🚀

### Quick Test (5 jobs):
```bash
cd /Users/olavopedal/Documents/GitHub/job_scrapers
source .venv/bin/activate
python test_updated_scraper.py
```

### Full Run:
```bash
python run_scraper.py
```

## Expected Output

```
INFO - Waiting for job listings to appear...
INFO - Results counter found - jobs should be present
INFO - Found elements with selector: div.ms-List-cell[role="listitem"]
INFO - Found 5 elements with selector: div.ms-List-cell[role="listitem"]
INFO - Verified 5 valid job elements
INFO - Processing 5 job elements (using selector: div.ms-List-cell[role="listitem"])
INFO - Scraped job 1/5: Machine Learning Engineer II
INFO - Scraped job 2/5: Senior Machine Learning Engineer
INFO - Scraped job 3/5: AI Research Scientist
...
INFO - Successfully scraped 5 jobs
INFO - Saved 5 jobs to output/microsoft_ai_jobs_20251004_123456.csv
```

## What Each Job Will Contain

```json
{
  "title": "Machine Learning Engineer II",
  "job_location": "Redmond, Washington, United States",
  "url": "https://careers.microsoft.com/us/en/job/1827725",
  "job_id": "1827725",
  "posted_date": "1 day ago",
  "description": "Viva Engage connects people through communities, bringing leaders and employees together...",
  "scraped_at": "2025-10-04T12:34:56",
  "source": "Microsoft Careers",
  "search_term": "AI",
  "location": "Seattle"
}
```

## Selector Priority

All selectors now have **TWO tiers**:

1. **Tier 1 (Primary):** Exact selectors from your manual inspection ⭐
2. **Tier 2 (Fallback):** Generic selectors in case Microsoft updates their UI

This means:
- ✅ Will work NOW with current Microsoft Careers page
- ✅ Will still work if they make minor changes (thanks to fallbacks)
- ✅ Easy to update if they completely redesign (just update Tier 1 selectors)

## Files Modified

✅ `microsoft_scraper.py` - All extraction methods updated with correct selectors
✅ `config.py` - Configuration updated with correct selectors
✅ `test_updated_scraper.py` - New test script created

## Why This Will Work

1. **Exact Match:** Using the exact classes and structure from the live page
2. **Icon-Based Location:** Finding location/date by their icons (stable)
3. **Aria Labels:** Using semantic aria-label for description (accessible & stable)
4. **Job ID Extraction:** Getting ID from aria-label (clean URL construction)
5. **Fallbacks:** Generic selectors as backup if Microsoft updates classes

## Verification Checklist

After running, verify:
- [ ] Found 5 job containers
- [ ] All titles extracted (not "N/A")
- [ ] All locations extracted (with full address)
- [ ] All dates extracted (e.g., "1 day ago")
- [ ] All descriptions extracted (100+ characters)
- [ ] All URLs constructed correctly
- [ ] Job IDs present in data

## If It Still Doesn't Work

If you still get 0 jobs, check the logs for:

```
INFO - Found X elements with selector: div.ms-List-cell[role="listitem"]
```

- **If X = 0:** The page structure changed. Re-run `manual_inspect.py`
- **If X > 0 but no jobs scraped:** The extraction selectors need adjustment
- **If "Verified 0 valid job elements":** The content validation is too strict

## Success Indicators

✅ Selector matches: `div.ms-List-cell[role="listitem"]`
✅ Count matches: 5 elements found = 5 results shown
✅ Data quality: Real job titles, locations, dates
✅ URLs work: Can open job posting in browser

---

**Status:** ✅ Ready to test with correct selectors
**Confidence:** High - using exact selectors from live page
**Next Step:** Run `python test_updated_scraper.py`
