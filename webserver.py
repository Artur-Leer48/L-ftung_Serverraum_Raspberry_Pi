from flask import Flask, jsonify, redirect, render_template, request, url_for

from app_state import get_state, set_temp_schwelle


app = Flask(__name__)


def _state_to_api(state):
    return {
        "temperature":           state["temperatur"],
        "temperature_f":         state["temperatur_fahrenheit"],
        "dew_point":             state["taupunkt"],
        "humidity":              state["luftfeuchte"],
        "pressure":              state["luftdruck"],
        "switch_on_temperature": state["temp_schwelle"],
        "fan_on":                state["luefter_aktiv"],
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/status")
def api_status():
    resp = jsonify(_state_to_api(get_state()))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.post("/api/settings")
def api_settings():
    data = request.get_json(force=True, silent=True) or {}
    try:
        threshold = float(data["switch_on_temperature"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "invalid switch_on_temperature"}), 400

    set_temp_schwelle(threshold)
    return jsonify(_state_to_api(get_state()))


# Legacy form endpoint kept for compatibility
@app.post("/threshold")
def set_threshold():
    set_temp_schwelle(float(request.form["temp_schwelle"]))
    return redirect(url_for("index"))


def run_webserver():
    app.run(host="0.0.0.0", port=8000)
