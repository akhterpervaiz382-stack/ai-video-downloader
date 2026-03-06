from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import yt_dlp

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(url_parts.query)
        video_url = params.get('url', [None])[0]

        if not video_url:
            self.send_error_response("No URL provided")
            return

        try:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                # Yeh data hamare HTML ko wapas jayega
                response_data = {
                    "status": "success",
                    "title": info.get('title', 'No Title'),
                    "thumbnail": info.get('thumbnail', ''),
                    "download_link": info.get('url', ''),
                    "summary": f"This video is about {info.get('title')}. It has {info.get('view_count', 0)} views and was uploaded by {info.get('uploader')}."
                }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_error_response(str(e))

    def send_error_response(self, message):
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "error", "message": message}).encode())
