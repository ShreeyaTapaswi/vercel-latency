from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/api/latency', methods=['GET', 'POST', 'OPTIONS'])
def latency():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

    if request.method == 'POST':
        payload = request.get_json(force=True, silent=True) or {}
        regions = payload.get('regions', None)
        threshold = payload.get('threshold_ms', None)
        filtered = data
        if regions:
            filtered = [d for d in filtered if d['region_group'] in regions]
        if threshold is not None:
            filtered = [d for d in filtered if d['latency'] > threshold]
        result = [{"region": d["region"], "latency": d["latency"]} for d in filtered]
        return jsonify(result)

    return jsonify(data)
