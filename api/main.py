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
        # Professional Headers to bypass blocks
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
            'nocheckcertificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info safely
            info = ydl.extract_info(url, download=False)
            
            # Formulating exact response for your HTML
            return {
                "status": "success",
                "title": info.get('title', 'Video Download Ready'),
                "thumbnail": info.get('thumbnail', ''),
                "download_link": info.get('url', ''),
                "summary": f"JarryLabs AI Analysis: Content from {info.get('uploader', 'Platform')} is processed and ready for high-speed download."
            }

    except Exception as e:
        # Check if it's a specific YouTube block error
        error_msg = str(e)
        if "403" in error_msg or "Sign in" in error_msg:
            return JSONResponse(content={"status": "error", "message": "YouTube is blocking the request. Try a different link or YouTube Short."}, status_code=500)
        
        return JSONResponse(content={"status": "error", "message": error_msg}, status_code=500)
