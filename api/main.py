from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/api/download")
async def download_video(url: str = Query(..., description="The video URL to download")):
    if not url:
        return JSONResponse(content={"status": "error", "message": "URL is missing"}, status_code=400)

    try:
        # Simple yt-dlp options for testing
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'allowed_extractors': ['youtube', 'tiktok', 'instagram', 'facebook'],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video information extract karna
            info = ydl.extract_info(url, download=False)
            
            # Formulating response
            return {
                "status": "success",
                "title": info.get('title', 'Video Download Ready'),
                "thumbnail": info.get('thumbnail', 'https://via.placeholder.com/300x200?text=JarryLabs+AI'),
                "download_link": info.get('url', ''),
                "summary": f"JarryLabs AI Analysis: This video by '{info.get('uploader', 'Unknown')}' is ready for download. Title: {info.get('title')}"
            }

    except Exception as e:
        # Agar koi error aaye to wo yahan se return hoga
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# Vercel backend ke liye root route
@app.get("/")
async def read_root():
    return {"status": "JarryLabs API is Live"}
