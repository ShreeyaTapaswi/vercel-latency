from fastapi import FastAPI
import numpy as np
import json
import os

app = FastAPI()

# Load telemetry JSON
telemetry_file = os.path.join(os.path.dirname(__file__), "../telemetry.json")
with open(telemetry_file) as f:
    telemetry_data = json.load(f)

@app.post("/api/latency")
async def latency_metrics(payload: dict):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)

    result = {}
    for region in regions:
        # Filter records by region
        region_records = [r for r in telemetry_data if r["region"] == region]
        if not region_records:
            result[region] = {"avg_latency": None, "p95_latency": None, "avg_uptime": None, "breaches": 0}
            continue

        latencies = [r["latency_ms"] for r in region_records]
        uptimes = [r["uptime"] for r in region_records]

        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        avg_uptime = np.mean(uptimes)
        breaches = sum(1 for l in latencies if l > threshold)

        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }

    return result
