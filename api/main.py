from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os
import requests

app = FastAPI()

def get_ai_summary(title):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return f"AI Insight: Video content is analyzed and ready."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    prompt = f"Write a 1-line catchy summary (max 12 words) for: {title}"
    
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=5)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return f"Summary: Ready to download '{title}'."

@app.get("/api/download")
async def download_video(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            # 'format_sort' help karta hai takay YouTube ko lage ye mobile app hai
            'format_sort': ['res:720', 'ext:mp4:m4a'],
            'quiet': True,
            'no_warnings': True,
            # 'extractor_args' YouTube ki bot detection ko dhoka dainay ke liye
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'skip': ['webpage']
                }
            },
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/19.08.35 (Linux; U; Android 11) (HIUI 12.5.4)',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Video')
            summary = get_ai_summary(video_title)

            return {
                "status": "success",
                "title": video_title,
                "thumbnail": info.get('thumbnail', ''),
                "download_link": info.get('url', ''),
                "summary": summary
            }
    except Exception as e:
        # Error message ko clean karna
        err_msg = str(e)
        if "Sign in to confirm you’re not a bot" in err_msg:
            err_msg = "YouTube Security Blocked this request. Try a TikTok or Instagram link to verify it works!"
        return JSONResponse(content={"status": "error", "message": err_msg}, status_code=500)
