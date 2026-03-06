from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/api/download")
async def download_video(url: str = Query(..., description="The video URL")):
    if not url:
        return JSONResponse(content={"status": "error", "message": "URL missing"}, status_code=400)

    try:
        # Mazeed advance headers jo YouTube blocks ko bypass karte hain
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'nocheckcertificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Sirf metadata nikalna hai (download nahi karna server par)
            info = ydl.extract_info(url, download=False)
            
            # Agar video link mil jaye to return karein
            return {
                "status": "success",
                "title": info.get('title', 'Video Download Ready'),
                "thumbnail": info.get('thumbnail', ''),
                "download_link": info.get('url', ''), # Direct link to MP4
                "summary": f"JarryLabs AI: This video is ready in high quality. Size might vary based on your connection."
            }

    except Exception as e:
        # Vercel logs mein check karne ke liye print karein
        print(f"Error details: {str(e)}")
        return JSONResponse(content={"status": "error", "message": "Server Busy or Link Blocked. Please try a YouTube Short or TikTok link to test."}, status_code=500)
