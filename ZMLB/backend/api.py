from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')  # ← disables GUI, uses non-interactive backend
import matplotlib.pyplot as plt
from ZMLB.backend.hybrid_insight_engine import generate_combined_insights
from ZMLB.backend.trends import plot_health_trends
# from .hybrid_insight_engine import generate_combined_insights
# from .trends import plot_health_trends

app = Flask(__name__)

# added cors here frontend
CORS(app, origins=["http://localhost:3000",
    "https://devulapellykushalhig.vercel.app"])

#csv routehandler
@app.route('/upload-csv/', methods=['POST'])
def upload_csv():
    print("🚀 Incoming request to /upload-csv")
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files allowed"}), 400       
        df = pd.read_csv(file)
        print("User data:\n", df.head())
        insights = generate_combined_insights(df)
        fig = plot_health_trends(df)
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=200, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        return jsonify({
            "insights": insights,
            "trend_image": img_str
        })
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
