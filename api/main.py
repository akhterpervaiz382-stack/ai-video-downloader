from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Sirf tabhi kaam kare jab URL mein /api/download ho
        message = {
            "status": "success",
            "message": "Backend is ready to download!",
            "info": "Use /api/download?url=YOUR_LINK to fetch video data."
        }
        self.wfile.write(json.dumps(message).encode())
