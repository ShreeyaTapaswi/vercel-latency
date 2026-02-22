from http.server import BaseHTTPRequestHandler
import json
import numpy as np

DATA = [
  {"region":"apac","latency_ms":124.83,"uptime_pct":99.323},
  {"region":"apac","latency_ms":227.12,"uptime_pct":97.911},
  {"region":"apac","latency_ms":139.3,"uptime_pct":99.139},
  {"region":"apac","latency_ms":237.77,"uptime_pct":98.938},
  {"region":"apac","latency_ms":143.19,"uptime_pct":98.876},
  {"region":"apac","latency_ms":138.79,"uptime_pct":97.116},
  {"region":"apac","latency_ms":236.29,"uptime_pct":98.591},
  {"region":"apac","latency_ms":156.94,"uptime_pct":99.278},
  {"region":"apac","latency_ms":177.3,"uptime_pct":99.081},
  {"region":"apac","latency_ms":207.03,"uptime_pct":98.761},
  {"region":"apac","latency_ms":156.32,"uptime_pct":98.594},
  {"region":"apac","latency_ms":176.99,"uptime_pct":97.148},
  {"region":"emea","latency_ms":197.21,"uptime_pct":98.686},
  {"region":"emea","latency_ms":145.85,"uptime_pct":97.973},
  {"region":"emea","latency_ms":152.56,"uptime_pct":97.395},
  {"region":"emea","latency_ms":228.19,"uptime_pct":98.347},
  {"region":"emea","latency_ms":146.51,"uptime_pct":98.5},
  {"region":"emea","latency_ms":120.38,"uptime_pct":99.086},
  {"region":"emea","latency_ms":154.49,"uptime_pct":98.158},
  {"region":"emea","latency_ms":205.96,"uptime_pct":97.304},
  {"region":"emea","latency_ms":175.45,"uptime_pct":98.557},
  {"region":"emea","latency_ms":160.83,"uptime_pct":99.166},
  {"region":"emea","latency_ms":106.66,"uptime_pct":97.434},
  {"region":"emea","latency_ms":121.09,"uptime_pct":98.065},
  {"region":"amer","latency_ms":219.63,"uptime_pct":97.333},
  {"region":"amer","latency_ms":116.22,"uptime_pct":98.068},
  {"region":"amer","latency_ms":156.39,"uptime_pct":99.197},
  {"region":"amer","latency_ms":196.48,"uptime_pct":97.391},
  {"region":"amer","latency_ms":184.89,"uptime_pct":97.669},
  {"region":"amer","latency_ms":221.29,"uptime_pct":97.992},
  {"region":"amer","latency_ms":185.15,"uptime_pct":97.832},
  {"region":"amer","latency_ms":141.59,"uptime_pct":97.611},
  {"region":"amer","latency_ms":137.72,"uptime_pct":98.875},
  {"region":"amer","latency_ms":186.34,"uptime_pct":97.176},
  {"region":"amer","latency_ms":162.95,"uptime_pct":97.275},
  {"region":"amer","latency_ms":145.03,"uptime_pct":98.529},
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        regions = body.get('regions', [])
        threshold = body.get('threshold_ms', 200)

        result = {}
        for region in regions:
            records = [d for d in DATA if d['region'] == region]
            if not records:
                continue
            latencies = [r['latency_ms'] for r in records]
            uptimes = [r['uptime_pct'] for r in records]
            result[region] = {
                "avg_latency": round(float(np.mean(latencies)), 4),
                "p95_latency": round(float(np.percentile(latencies, 95)), 4),
                "avg_uptime": round(float(np.mean(uptimes)), 4),
                "breaches": int(sum(1 for l in latencies if l > threshold))
            }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"regions": result}).encode())
