from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import requests

app = FastAPI()

@app.get("/api/download")
async def download_video(url: str = Query(..., description="The video URL to download")):
    if not url:
        return JSONResponse(content={"status": "error", "message": "No URL provided"}, status_code=400)

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Metadata extract karna
            video_title = info.get('title', 'No Title')
            thumbnail = info.get('thumbnail', '')
            download_url = info.get('url', '')
            uploader = info.get('uploader', 'Unknown')

            # Temporary AI Summary (Jab tak Gemini API Key nahi daltay)
            ai_summary = f"JarryLabs AI Analysis: This video by '{uploader}' titled '{video_title}' is ready for high-quality download."

            return {
                "status": "success",
                "title": video_title,
                "thumbnail": thumbnail,
                "download_link": download_url,
                "summary": ai_summary
            }

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# Vercel ko FastAPI app chalane ke liye ye zaroori hai
@app.get("/")
async def root():
    return {"message": "JarryLabs API is Running"}
