"""
Simple test endpoint to verify Python works on Vercel
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = json.dumps({
            "status": "ok",
            "message": "Python is working on Vercel",
            "endpoint": "test"
        })

        self.wfile.write(response.encode())
        return
