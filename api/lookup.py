from http.server import BaseHTTPRequestHandler
import requests
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            
            # Get mobile number from query
            mobile = params.get('mobile', [None])[0]
            
            if not mobile:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Mobile number is required",
                    "usage": "/api/lookup?mobile=9811790070"
                }).encode())
                return
            
            # Call the original API
            original_url = f"https://ethicaltabbo.in/api/lookup?key=Sahil&mobile={mobile}"
            response = requests.get(original_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Clean the data - remove unwanted fields
                if 'telegram' in data:
                    del data['telegram']
                if 'channel' in data:
                    del data['channel']
                if 'credit' in data:
                    del data['credit']
                if 'api_info' in data:
                    del data['api_info']
                
                # Remove unwanted fields from each record
                if 'data' in data and data['data']:
                    for record in data['data']:
                        if 'id' in record:
                            del record['id']
                        if 'alt_number' in record:
                            del record['alt_number']
                
                # Add credit to response
                data['credit'] = "GENIUS HACKER 29 API"
                data['developer'] = "ADIBHAI"
                data['youtube'] = "https://youtube.com/@geniushacker29"
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode())
            else:
                self.send_response(response.status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Original API returned error",
                    "status": response.status_code
                }).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
