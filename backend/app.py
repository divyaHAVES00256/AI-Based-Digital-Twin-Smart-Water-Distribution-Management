from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from simulation import run_simulation

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "test_ann_predictions_2500_rows.csv")

def load_demands():
    df = pd.read_csv(CSV_PATH)
    return df["predicted_demand"].tolist()

@app.route("/api/simulate", methods=["POST"])
def simulate():
    try:
        body = request.get_json()
        scenario      = body.get("scenario", "normal")
        tank_initial  = float(body.get("tank_initial", 50))
        pump_input    = float(body.get("pump_input", 60))
        leak_prob     = float(body.get("leak_probability", 0))
        tank_max      = float(body.get("tank_max", 100))

        demands = load_demands()

        result = run_simulation(
            demands=demands,
            leak_probability=leak_prob,
            tank_initial=tank_initial,
            pump_input=pump_input,
            tank_max=tank_max,
            scenario=scenario
        )

        # Build alert list
        alerts = []
        for i, (tank, lp) in enumerate(zip(result["tank_levels"], [leak_prob] * len(result["tank_levels"]))):
            if tank < 10:
                alerts.append({"step": i, "message": "Low Tank Level", "type": "danger"})
            elif leak_prob > 0.6:
                alerts.append({"step": i, "message": "Possible Leak Detected", "type": "warning"})

        # Deduplicate consecutive same-type alerts (keep first occurrence per run)
        seen = set()
        unique_alerts = []
        for a in alerts:
            key = a["message"]
            if key not in seen:
                seen.add(key)
                unique_alerts.append(a)

        # Summary stats
        tank_levels = result["tank_levels"]
        pressures   = result["pressures"]
        demands_out = result["demands"]

        summary = {
            "avg_tank":     round(sum(tank_levels) / len(tank_levels), 2),
            "min_tank":     round(min(tank_levels), 2),
            "max_tank":     round(max(tank_levels), 2),
            "avg_pressure": round(sum(pressures) / len(pressures), 2),
            "max_pressure": round(max(pressures), 2),
            "avg_demand":   round(sum(demands_out) / len(demands_out), 2),
            "alert_count":  len(unique_alerts),
            "total_steps":  len(tank_levels),
        }

        return jsonify({
            "success": True,
            "tank_levels":  [round(v, 2) for v in tank_levels],
            "pressures":    [round(v, 2) for v in pressures],
            "demands":      [round(v, 2) for v in demands_out],
            "leak_losses":  [round(v, 2) for v in result["leak_losses"]],
            "alerts":       unique_alerts,
            "summary":      summary,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "demands_loaded": len(load_demands())})


if __name__ == "__main__":
    print("Starting Digital Twin API on http://localhost:5000")
    app.run(debug=True, port=5000)
