from fastapi import FastAPI
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = [ ... ]  # your full dataset

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

@app.post("/api/latency")
async def latency_metrics(payload: dict):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)
    filtered = DATA
    if regions:
        filtered = [d for d in DATA if d["region"] in regions]
    grouped = {}
    for d in filtered:
        r = d["region"]
        if r not in grouped:
            grouped[r] = []
        grouped[r].append(d)
    response = {rg: compute(recs, threshold) for rg, recs in grouped.items()}
    return response
