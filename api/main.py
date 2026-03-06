import tempfile

@app.get("/api/download")
async def download_video(url: str = Query(..., description="Video URL")):
    try:
        # Cookies ko temporary file mein save karna
        cookie_content = os.getenv("YT_COOKIES")
        cookie_path = None
        
        if cookie_content:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
                tmp.write(cookie_content)
                cookie_path = tmp.name

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_path, # Cookies yahan use ho rahi hain
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Video')
            summary = get_ai_summary(video_title)

            # Cleanup temporary file
            if cookie_path:
                os.remove(cookie_path)

            return {
                "status": "success",
                "title": video_title,
                "thumbnail": info.get('thumbnail', ''),
                "download_link": info.get('url', ''),
                "summary": summary
            }
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
