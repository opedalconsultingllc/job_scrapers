# Quick Fix Summary - Job Elements Issue

## The Problem

The scraper sees the results counter `<h1>Showing 1-5 of 5 results</h1>` but isn't finding the actual job elements below it.

## Likely Causes

1. **Jobs are in a specific container** that we're not targeting
2. **Dynamic content loading** - Jobs may load after the page appears ready
3. **Shadow DOM or iframe** - Jobs might be in an isolated context
4. **Specific Microsoft UI components** - Using Fabric UI or custom components

## Immediate Actions

### 1. Run the Job Element Inspector

```bash
cd /Users/olavopedal/Documents/GitHub/job_scrapers
source .venv/bin/activate
python inspect_job_elements.py
```

This will:
- ✅ Navigate to results page
- ✅ Find all potential job containers
- ✅ Analyze element structure
- ✅ Take a screenshot
- ✅ Save detailed analysis to JSON
- ✅ Stay open for 30s for manual inspection

### 2. Check the Output Files

After running:
```bash
# View the analysis
cat job_elements_analysis.json | python -m json.tool

# View the screenshot
open job_results_screenshot.png
```

### 3. Manual Inspection Steps

While the browser is open:

1. **Right-click on a job title** → Inspect
2. **Look at the parent elements** going up the tree
3. **Find the container** that wraps ONE job
4. **Note down:**
   - Container tag name (e.g., `div`, `li`, `article`)
   - Container classes (e.g., `job-card`, `ms-List-cell`)
   - Any `data-*` attributes (e.g., `data-job-id`)

### 4. Common Microsoft Careers Patterns

Based on typical Microsoft web apps, jobs might be in:

```html
<!-- Pattern 1: List with role attributes -->
<ul role="list">
  <li role="listitem" class="ms-List-cell">
    <div class="job-card">
      <h2>Job Title</h2>
      ...
    </div>
  </li>
</ul>

<!-- Pattern 2: Div-based cards -->
<div class="search-results">
  <div class="job-card" data-job-id="12345">
    <h2>Job Title</h2>
    ...
  </div>
</div>

<!-- Pattern 3: Article elements -->
<div class="results-container">
  <article class="job-listing">
    <h2>Job Title</h2>
    ...
  </article>
</div>
```

### 5. Update Scraper Based on Findings

Once you know the actual structure, update the `listing_selectors` array in `microsoft_scraper.py`:

```python
listing_selectors = [
    'YOUR_ACTUAL_SELECTOR',  # Add the real selector at the top
    '[role="listitem"]',
    '[data-job-id]',
    # ... rest of selectors
]
```

## Debugging Checklist

- [ ] Run `inspect_job_elements.py`
- [ ] Check `job_elements_analysis.json` for findings
- [ ] View `job_results_screenshot.png`
- [ ] Manually inspect in browser (Dev Tools)
- [ ] Note the exact selector for ONE job
- [ ] Update `microsoft_scraper.py` with correct selector
- [ ] Test the scraper again

## Quick Test After Fix

```bash
# Test with just 5 jobs
python -c "
import asyncio
from microsoft_scraper import MicrosoftCareersScraper

async def test():
    scraper = MicrosoftCareersScraper(headless=False)
    jobs = await scraper.scrape('AI', 'Seattle', 5)
    print(f'Found {len(jobs)} jobs')
    if jobs:
        print(f'First job: {jobs[0].get(\"title\")}')

asyncio.run(test())
"
```

## Next Steps

1. Wait for inspector to finish (30 seconds)
2. Check the generated files
3. Share the findings if you need help interpreting them
4. Update the selector based on what we find

---

**Status:** 🔍 Inspector running...
