from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os
import requests

app = FastAPI()

def get_ai_summary(title):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return f"Video Ready: {title}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": f"Write a 1-line summary: {title}"}]}]}, timeout=5)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except: return f"Title: {title}"

@app.get("/api/download")
async def download_video(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            'format': 'best',
            # Yahan hum YouTube ko dhoka dene ke liye special 'clients' use kar rahe hain
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web_embedded', 'tv'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "status": "success",
                "title": info.get('title', 'Video'),
                "thumbnail": info.get('thumbnail', ''),
                "download_link": info.get('url', ''),
                "summary": get_ai_summary(info.get('title', 'Video'))
            }
    except Exception as e:
        # Agar block ho jaye, to error ko clean dikhayen
        return JSONResponse(content={"status": "error", "message": "YouTube Security is tight. Try a Short or Reel instead."}, status_code=500)
