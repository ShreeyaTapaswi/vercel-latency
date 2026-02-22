from fastapi import FastAPI
import numpy as np

app = FastAPI()

# Dummy telemetry embedded (no file needed)
telemetry_data = [
    {"region": "emea", "latency_ms": 120, "uptime": 0.99},
    {"region": "emea", "latency_ms": 190, "uptime": 0.98},
    {"region": "amer", "latency_ms": 150, "uptime": 0.97},
    {"region": "amer", "latency_ms": 210, "uptime": 0.96}
]

@app.post("/api/latency")
async def latency_metrics(payload: dict):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)

    result = {}
    for region in regions:
        region_records = [r for r in telemetry_data if r["region"] == region]
        if not region_records:
            result[region] = {"avg_latency": None, "p95_latency": None, "avg_uptime": None, "breaches": 0}
            continue

        latencies = [r["latency_ms"] for r in region_records]
        uptimes = [r["uptime"] for r in region_records]

        result[region] = {
            "avg_latency": round(np.mean(latencies), 2),
            "p95_latency": round(np.percentile(latencies, 95), 2),
            "avg_uptime": round(np.mean(uptimes), 2),
            "breaches": sum(1 for l in latencies if l > threshold)
        }

    return result
