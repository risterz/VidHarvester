from __future__ import annotations

import asyncio
from typing import List

from playwright.async_api import async_playwright

from vidharvester.utils.logger import get_logger


_log = get_logger("capture.playwright")


async def capture_page_media(url: str, timeout_ms: int = 30000) -> List[str]:
    """Use Playwright to open a page headlessly and collect media manifest/segment URLs.
    
    Args:
        url: URL to navigate to
        timeout_ms: Page load timeout in milliseconds
        
    Returns:
        List of candidate media URLs found
    """
    media_urls = set()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Listen for network responses
        def handle_response(response):
            response_url = response.url
            content_type = response.headers.get("content-type", "")
            
            # Look for video/audio content types or manifest files
            if any(ext in response_url.lower() for ext in [".m3u8", ".mpd", ".mp4", ".webm", ".avi", ".mov"]):
                media_urls.add(response_url)
            elif any(ct in content_type.lower() for ct in ["video/", "audio/", "application/dash+xml", "application/vnd.apple.mpegurl"]):
                media_urls.add(response_url)
        
        page.on("response", handle_response)
        
        try:
            await page.goto(url, timeout=timeout_ms)
            # Wait a bit for dynamic content
            await page.wait_for_timeout(3000)
        except Exception as exc:
            _log.warning("Failed to load page %s: %s", url, exc)
        finally:
            await browser.close()
    
    return list(media_urls)
