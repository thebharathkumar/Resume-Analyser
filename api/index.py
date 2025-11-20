"""
Vercel Python Serverless Function - Native format with proper multipart handling
"""
from http.server import BaseHTTPRequestHandler
import json
import uuid
from pathlib import Path
import cgi
from io import BytesIO

ALLOWED_EXTENSIONS = ["pdf", "docx", "doc"]
MAX_SIZE = 10 * 1024 * 1024  # 10MB

class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/health':
            self._send_json({"status": "healthy", "version": "1.0.0"})
        elif self.path == '/':
            self._send_json({"status": "ok", "message": "API is running"})
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        try:
            if self.path == '/api/upload/':
                self._handle_upload()
            elif self.path == '/api/analyze/':
                self._handle_analyze()
            else:
                self._send_json({"error": "Not found"}, 404)
        except Exception as e:
            print(f"Error in POST: {e}")
            import traceback
            traceback.print_exc()
            self._send_json({"error": str(e), "detail": "Internal server error"}, 500)

    def _handle_upload(self):
        try:
            # Get content type and length
            content_type = self.headers.get('Content-Type', '')
            content_length = int(self.headers.get('Content-Length', 0))

            if not content_type or 'multipart/form-data' not in content_type:
                self._send_json({"error": "Content-Type must be multipart/form-data"}, 400)
                return

            # Read the body
            body = self.rfile.read(content_length)

            # Parse using cgi.FieldStorage
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': content_type,
                'CONTENT_LENGTH': str(content_length),
            }

            form = cgi.FieldStorage(
                fp=BytesIO(body),
                environ=environ,
                keep_blank_values=True
            )

            # Get the file field
            if 'file' not in form:
                self._send_json({"error": "No file field in upload"}, 400)
                return

            file_item = form['file']

            if not file_item.filename:
                self._send_json({"error": "No file selected"}, 400)
                return

            filename = file_item.filename
            file_data = file_item.file.read()

            # Validate extension
            ext = filename.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                self._send_json({
                    "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                }, 400)
                return

            # Validate size
            if len(file_data) > MAX_SIZE:
                self._send_json({"error": "File too large (max 10MB)"}, 400)
                return

            # Save file
            file_id = str(uuid.uuid4())
            upload_dir = Path("/tmp/resume-uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_path = upload_dir / f"{file_id}.{ext}"
            file_path.write_bytes(file_data)

            self._send_json({
                "file_id": file_id,
                "filename": filename,
                "file_type": ext,
                "size": len(file_data),
                "message": "Upload successful"
            })

        except Exception as e:
            print(f"Upload error: {e}")
            import traceback
            traceback.print_exc()
            self._send_json({"error": str(e)}, 500)

    def _handle_analyze(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode())
            except:
                self._send_json({"error": "Invalid JSON"}, 400)
                return

            file_id = data.get('file_id')
            if not file_id:
                self._send_json({"error": "file_id required"}, 400)
                return

            # Check if file exists
            upload_dir = Path("/tmp/resume-uploads")
            found = False
            for ext in ALLOWED_EXTENSIONS:
                if (upload_dir / f"{file_id}.{ext}").exists():
                    found = True
                    break

            if not found:
                self._send_json({"error": "File not found"}, 404)
                return

            # Return mock analysis
            self._send_json({
                "analysis_id": str(uuid.uuid4()),
                "file_id": file_id,
                "ats_score": 85,
                "overall_score": 82,
                "keyword_score": 78,
                "formatting_score": 90,
                "readability_score": 80,
                "sections_found": ["Summary", "Experience", "Education", "Skills"],
                "key_findings": [
                    "Strong technical skills section",
                    "Clear work experience descriptions",
                    "Good use of action verbs"
                ],
                "recommendations": [
                    "Add more quantifiable achievements",
                    "Include relevant keywords",
                    "Consider adding a skills summary"
                ],
                "keywords_found": ["Python", "JavaScript", "ML", "Data Analysis"],
                "missing_keywords": ["Cloud", "DevOps", "Agile"],
                "status": "completed"
            })

        except Exception as e:
            print(f"Analyze error: {e}")
            import traceback
            traceback.print_exc()
            self._send_json({"error": str(e)}, 500)
