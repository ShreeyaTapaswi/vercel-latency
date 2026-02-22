import json
from http.server import BaseHTTPRequestHandler

data = [
    {"region": "us-east-1", "region_group": "amer", "latency": 245},
    {"region": "us-east-2", "region_group": "amer", "latency": 260},
    {"region": "us-west-1", "region_group": "amer", "latency": 310},
    {"region": "us-west-2", "region_group": "amer", "latency": 290},
    {"region": "eu-west-1", "region_group": "emea", "latency": 180},
    {"region": "eu-west-2", "region_group": "emea", "latency": 195},
    {"region": "eu-central-1", "region_group": "emea", "latency": 175},
    {"region": "ap-south-1", "region_group": "apac", "latency": 320},
    {"region": "ap-southeast-1", "region_group": "apac", "latency": 280},
    {"region": "ap-southeast-2", "region_group": "apac", "latency": 350},
    {"region": "ap-northeast-1", "region_group": "apac", "latency": 270},
    {"region": "ap-northeast-2", "region_group": "apac", "latency": 285},
    {"region": "sa-east-1", "region_group": "amer", "latency": 400},
    {"region": "ca-central-1", "region_group": "amer", "latency": 230},
    {"region": "me-south-1", "region_group": "emea", "latency": 380}
]

class handler(BaseHTTPRequestHandler):
    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body)
        except:
            payload = {}

        regions = payload.get('regions', None)
        threshold = payload.get('threshold_ms', None)

        filtered = data
        if regions:
            filtered = [d for d in filtered if d['region_group'] in regions]
        if threshold is not None:
            filtered = [d for d in filtered if d['latency'] > threshold]

        result = [{"region": d["region"], "latency": d["latency"]} for d in filtered]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
