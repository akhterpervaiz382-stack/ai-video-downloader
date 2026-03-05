from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/api/download")
def download_video(url: str = Query(..., description="Video URL to fetch")):
    try:
        ydl_opts = {'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Simple AI summary for now
            summary = f"Video Title: {info.get('title')}. Duration: {info.get('duration')}s."
            
            return {
                "status": "success",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "download_link": info.get('url'),
                "summary": summary
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    return {"message": "AI Video Downloader API is running!"}
