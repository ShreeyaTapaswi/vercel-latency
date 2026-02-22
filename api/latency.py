import json
from http.server import BaseHTTPRequestHandler

DATA = [
  {"region": "apac", "latency_ms": 124.83, "uptime_pct": 99.323},
  {"region": "apac", "latency_ms": 227.12, "uptime_pct": 97.911},
  {"region": "apac", "latency_ms": 139.3, "uptime_pct": 99.139},
  {"region": "apac", "latency_ms": 237.77, "uptime_pct": 98.938},
  {"region": "apac", "latency_ms": 143.19, "uptime_pct": 98.876},
  {"region": "apac", "latency_ms": 138.79, "uptime_pct": 97.116},
  {"region": "apac", "latency_ms": 236.29, "uptime_pct": 98.591},
  {"region": "apac", "latency_ms": 156.94, "uptime_pct": 99.278},
  {"region": "apac", "latency_ms": 177.3, "uptime_pct": 99.081},
  {"region": "apac", "latency_ms": 207.03, "uptime_pct": 98.761},
  {"region": "apac", "latency_ms": 156.32, "uptime_pct": 98.594},
  {"region": "apac", "latency_ms": 176.99, "uptime_pct": 97.148},
  {"region": "emea", "latency_ms": 197.21, "uptime_pct": 98.686},
  {"region": "emea", "latency_ms": 145.85, "uptime_pct": 97.973},
  {"region": "emea", "latency_ms": 152.56, "uptime_pct": 97.395},
  {"region": "emea", "latency_ms": 228.19, "uptime_pct": 98.347},
  {"region": "emea", "latency_ms": 146.51, "uptime_pct": 98.5},
  {"region": "emea", "latency_ms": 120.38, "uptime_pct": 99.086},
  {"region": "emea", "latency_ms": 154.49, "uptime_pct": 98.158},
  {"region": "emea", "latency_ms": 205.96, "uptime_pct": 97.304},
  {"region": "emea", "latency_ms": 175.45, "uptime_pct": 98.557},
  {"region": "emea", "latency_ms": 160.83, "uptime_pct": 99.166},
  {"region": "emea", "latency_ms": 106.66, "uptime_pct": 97.434},
  {"region": "emea", "latency_ms": 121.09, "uptime_pct": 98.065},
  {"region": "amer", "latency_ms": 219.63, "uptime_pct": 97.333},
  {"region": "amer", "latency_ms": 116.22, "uptime_pct": 98.068},
  {"region": "amer", "latency_ms": 156.39, "uptime_pct": 99.197},
  {"region": "amer", "latency_ms": 196.48, "uptime_pct": 97.391},
  {"region": "amer", "latency_ms": 184.89, "uptime_pct": 97.669},
  {"region": "amer", "latency_ms": 221.29, "uptime_pct": 97.992},
  {"region": "amer", "latency_ms": 185.15, "uptime_pct": 97.832},
  {"region": "amer", "latency_ms": 141.59, "uptime_pct": 97.611},
  {"region": "amer", "latency_ms": 137.72, "uptime_pct": 98.875},
  {"region": "amer", "latency_ms": 186.34, "uptime_pct": 97.176},
  {"region": "amer", "latency_ms": 162.95, "uptime_pct": 97.275},
  {"region": "amer", "latency_ms": 145.03, "uptime_pct": 98.529},
]

def compute(records, threshold):
    latencies = sorted([r["latency_ms"] for r in records])
    uptimes = [r["uptime_pct"] for r in records]
    n = len(latencies)
    avg_latency = round(sum(latencies) / n, 2)
    idx = 0.95 * (n - 1)
    lower = int(idx)
    upper = min(lower + 1, n - 1)
    p95 = round(latencies[lower] + (idx - lower) * (latencies[upper] - latencies[lower]), 2)
    avg_uptime = round(sum(uptimes) / len(uptimes), 2)
    breaches = sum(1 for l in latencies if l > threshold)
    return {"avg_latency": avg_latency, "p95_latency": p95, "avg_uptime": avg_uptime, "breaches": breaches}

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(DATA).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except:
            payload = {}

        regions = payload.get('regions', None)
        threshold = payload.get('threshold_ms', 0)

        filtered = DATA
        if regions:
            filtered = [d for d in DATA if d['region'] in regions]

        grouped = {}
        for d in filtered:
            r = d['region']
            if r not in grouped:
                grouped[r] = []
            grouped[r].append(d)

        response = {rg: compute(recs, threshold) for rg, recs in grouped.items()}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
