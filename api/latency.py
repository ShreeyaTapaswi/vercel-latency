import json
from http.server import BaseHTTPRequestHandler

data = [
    {"region":"us-east-1","latency":245},{"region":"us-east-2","latency":260},
    {"region":"us-west-1","latency":310},{"region":"us-west-2","latency":290},
    {"region":"eu-west-1","latency":180},{"region":"eu-west-2","latency":195},
    {"region":"eu-central-1","latency":175},{"region":"ap-south-1","latency":320},
    {"region":"ap-southeast-1","latency":280},{"region":"ap-southeast-2","latency":350},
    {"region":"ap-northeast-1","latency":270},{"region":"ap-northeast-2","latency":285},
    {"region":"sa-east-1","latency":400},{"region":"ca-central-1","latency":230},
    {"region":"me-south-1","latency":380}
]

def compute_stats():
    latencies = [d["latency"] for d in data]
    sorted_l = sorted(latencies)
    n = len(sorted_l)
    mean = sum(sorted_l) / n
    def percentile(p):
        idx = (p / 100) * (n - 1)
        lower = int(idx)
        upper = min(lower + 1, n - 1)
        return sorted_l[lower] + (idx - lower) * (sorted_l[upper] - sorted_l[lower])
    return {
        "mean": round(mean, 2),
        "p50": round(percentile(50), 2),
        "p95": round(percentile(95), 2),
        "p99": round(percentile(99), 2)
    }

class handler(BaseHTTPRequestHandler):
    def _send_response(self):
        stats = compute_stats()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self._send_response()

    def do_POST(self):
        self._send_response()
