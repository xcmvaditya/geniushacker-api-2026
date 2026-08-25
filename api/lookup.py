import requests
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL
            parsed_path = urlparse(self.path)
            params = parse_qs(parsed_path.query)
            
            # Get mobile number
            mobile = params.get('mobile', [None])[0]
            
            # If no mobile parameter
            if not mobile:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": False,
                    "error": "Mobile number required",
                    "usage": "/api/lookup?mobile=9876543210"
                }).encode())
                return
            
            # Call the original API
            original_url = f"https://ethicaltabbo.in/api/lookup?key=Sahil&mobile={mobile}"
            response = requests.get(original_url, timeout=15)
            
            # Handle API response
            if response.status_code == 200:
                data = response.json()
                
                # Clean data - remove unwanted fields
                for key in ['telegram', 'channel', 'credit', 'api_info']:
                    if key in data:
                        del data[key]
                
                # Remove unwanted fields from records
                if 'data' in data and data['data']:
                    for record in data['data']:
                        for key in ['id', 'alt_number']:
                            if key in record:
                                del record[key]
                
                # Add your branding
                data['credit'] = "GENIUS HACKER 29 API"
                data['developer'] = "ADIBHAI"
                data['youtube'] = "https://youtube.com/@geniushacker29"
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode())
            else:
                # Original API returned error
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": False,
                    "error": "Original API returned error",
                    "code": response.status_code
                }).encode())
                
        except requests.exceptions.Timeout:
            self.send_response(504)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": False,
                "error": "Request timeout - please try again"
            }).encode())
            
        except requests.exceptions.ConnectionError:
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": False,
                "error": "Connection error - API unreachable"
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": False,
                "error": str(e)
            }).encode())
