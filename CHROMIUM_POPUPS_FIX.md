# Chromium Pop-ups Fix for macOS 🔧

## Problem Description

When running the scraper on macOS, Chromium browser was showing notification permission pop-up dialogs that blocked the automation. These system-level dialogs were preventing the scraper from filling in the search form and progressing past the first page.

## Root Cause

macOS Chromium displays permission dialogs for:
1. **Notifications** - "Do you want to allow notifications?"
2. **Other permissions** - Location, camera, microphone, etc.

These dialogs are modal and block all automation until dismissed, causing the scraper to hang.

## Solution Implemented

### 1. Browser Launch Arguments (Primary Fix)

Added additional Chrome flags to disable notifications and pop-ups:

```python
self.browser = await self.playwright.chromium.launch(
    headless=self.headless,
    args=[
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-notifications',      # ✅ NEW: Disable notification prompts
        '--disable-popup-blocking',     # ✅ NEW: Prevent popup blocks
        '--disable-infobars',           # ✅ NEW: Disable info bars
    ]
)
```

### 2. Browser Context Permissions (Secondary Fix)

Configured the browser context to deny all permissions by default:

```python
self.context = await self.browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    locale='en-US',
    timezone_id='America/Los_Angeles',
    permissions=[],                     # ✅ NEW: Don't grant any permissions
    ignore_https_errors=True,           # ✅ NEW: Ignore HTTPS errors
)
```

### 3. Dialog Handler (Fallback Fix)

Added an automatic dialog handler to dismiss any remaining dialogs:

```python
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
```

This handler is automatically set up when a page is created in the `scrape()` method.

## What Changed

### Modified Files
- ✅ `microsoft_scraper.py` - Updated browser initialization and added dialog handler

### Changes Made
1. **Browser args**: Added `--disable-notifications`, `--disable-popup-blocking`, `--disable-infobars`
2. **Context config**: Added `permissions=[]` and `ignore_https_errors=True`
3. **New method**: `setup_dialog_handlers()` to handle any dialogs that still appear
4. **Integration**: Dialog handler is now called in the `scrape()` method

## Testing

All existing tests continue to pass:

```bash
pytest test_microsoft_scraper.py -v
# Result: 13 passed ✅
```

## Usage

No changes to the user interface! Just run as before:

```bash
python run_scraper.py
```

The scraper will now:
1. ✅ Not show notification permission pop-ups
2. ✅ Automatically dismiss any dialogs that appear
3. ✅ Continue filling in the search form without interruption
4. ✅ Progress beyond the first page to scrape jobs

## Additional Benefits

These fixes also help with:
- **Faster execution** - No waiting for dialogs
- **Better reliability** - No manual intervention needed
- **Cross-platform consistency** - Works better on macOS
- **Cleaner UI** - No distracting permission requests

## Verification

To verify the fix works:

1. Run the scraper:
   ```bash
   source .venv/bin/activate
   python run_scraper.py
   ```

2. Watch for:
   - ✅ No notification pop-ups appear
   - ✅ Search form is filled automatically
   - ✅ Browser navigates to results page
   - ✅ Jobs are scraped successfully

3. Check logs for dialog handling:
   ```
   INFO - Dialog handlers registered
   INFO - Searching for 'AI' jobs in 'Seattle'
   INFO - Found job title field: ...
   INFO - Search completed successfully
   ```

## Troubleshooting

If you still see pop-ups:

1. **Try headless mode** - May avoid some macOS dialogs:
   ```python
   scraper = MicrosoftCareersScraper(headless=True)
   ```

2. **Check system permissions** - Go to System Preferences > Security & Privacy > Privacy
   - Ensure Chromium has proper permissions
   - Reset permissions if needed

3. **Clear browser data** - Remove any saved preferences:
   ```bash
   rm -rf ~/Library/Application\ Support/com.microsoft.playwright/
   playwright install chromium
   ```

4. **Update Playwright** - Ensure you have the latest version:
   ```bash
   pip install --upgrade playwright
   playwright install chromium
   ```

## Technical Notes

- The `--disable-notifications` flag prevents the browser from requesting notification permissions
- The `permissions=[]` setting ensures no permissions are pre-granted
- The dialog handler uses Playwright's event system to catch and dismiss dialogs asynchronously
- These changes are specific to Chromium and may not affect other browsers

---

**Fixed on:** October 3, 2025  
**Tested on:** macOS with Python 3.12.11  
**Status:** ✅ Working
