from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os
import requests

app = FastAPI()

def get_gemini_summary(title):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return f"AI Insight: This video titled '{title}' is ready for download."
    
    prompt = f"Write a professional 1-line summary (max 12 words) for: {title}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return f"Ready to download: {title}"

@app.get("/api/download")
async def download_video(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Video')
            
            # AI Summary Generation
            summary = get_gemini_summary(video_title)

            return {
                "status": "success",
                "title": video_title,
                "thumbnail": info.get('thumbnail', ''),
                "download_link": info.get('url', ''),
                "summary": summary
            }
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
