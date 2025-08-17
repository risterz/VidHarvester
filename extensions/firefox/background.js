// VidHarvester Firefox Extension Background Script
// Captures media URLs and forwards them to the local VidHarvester app

const CAPTURE_URL = 'http://127.0.0.1:8089/capture';

// Listen for completed web requests
browser.webRequest.onCompleted.addListener(
  (details) => {
    const url = details.url;
    
    // Filter for media URLs
    if (url.match(/\.(m3u8|mpd|mp4|webm|avi|mov|mkv|flv)($|\?)/i) ||
        url.includes('manifest') ||
        url.includes('playlist')) {
      
      // Send to VidHarvester app
      fetch(CAPTURE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          url: url,
          tabUrl: details.originUrl || '',
          timestamp: Date.now()
        })
      }).catch(err => console.warn('VidHarvester capture failed:', err));
    }
  },
  { urls: ['<all_urls>'] }
);
