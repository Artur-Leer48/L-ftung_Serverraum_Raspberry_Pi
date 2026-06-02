from flask import Flask, redirect, render_template_string, request, url_for

from app_state import get_state, set_temp_schwelle


app = Flask(__name__)


HTML = """
<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="5">
    <title>Lüftersteuerung</title>
    <style>
        :root {
            color-scheme: light;
            font-family: Arial, sans-serif;
            background: #f3f5f7;
            color: #17202a;
        }

        body {
            margin: 0;
        }

        main {
            max-width: 920px;
            margin: 0 auto;
            padding: 32px 20px;
        }

        h1 {
            margin: 0 0 24px;
            font-size: 32px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
        }

        .card {
            background: #ffffff;
            border: 1px solid #d9e0e7;
            border-radius: 8px;
            padding: 18px;
        }

        .label {
            color: #5d6d7e;
            font-size: 14px;
            margin-bottom: 8px;
        }

        .value {
            font-size: 28px;
            font-weight: 700;
        }

        .status {
            color: {{ '#137333' if state.luefter_aktiv else '#9a3412' }};
        }

        form {
            display: flex;
            gap: 12px;
            align-items: end;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        input {
            border: 1px solid #b8c4d0;
            border-radius: 6px;
            font-size: 18px;
            padding: 9px 10px;
            width: 140px;
        }

        button {
            border: 0;
            border-radius: 6px;
            background: #2563eb;
            color: white;
            font-size: 16px;
            padding: 11px 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <main>
        <h1>Lüftersteuerung</h1>
        <section class="grid">
            <div class="card">
                <div class="label">Temperatur</div>
                <div class="value">{{ format_value(state.temperatur, '%.2f °C') }}</div>
            </div>
            <div class="card">
                <div class="label">Temperatur</div>
                <div class="value">{{ format_value(state.temperatur_fahrenheit, '%.2f °F') }}</div>
            </div>
            <div class="card">
                <div class="label">Taupunkt</div>
                <div class="value">{{ format_value(state.taupunkt, '%.2f °C') }}</div>
            </div>
            <div class="card">
                <div class="label">Luftfeuchte</div>
                <div class="value">{{ format_value(state.luftfeuchte, '%.0f %%') }}</div>
            </div>
            <div class="card">
                <div class="label">Luftdruck</div>
                <div class="value">{{ format_value(state.luftdruck, '%.0f hPa') }}</div>
            </div>
            <div class="card">
                <div class="label">Lüfter</div>
                <div class="value status">{{ 'AN' if state.luefter_aktiv else 'AUS' }}</div>
            </div>
        </section>

        <section class="card" style="margin-top: 16px;">
            <div class="label">Einschalttemperatur</div>
            <form method="post" action="{{ url_for('set_threshold') }}">
                <input type="number" name="temp_schwelle" step="0.1" value="{{ '%.1f' % state.temp_schwelle }}" required>
                <button type="submit">Speichern</button>
            </form>
        </section>
    </main>
</body>
</html>
"""


def format_value(value, pattern):
    if value is None:
        return "-"

    return pattern % value


@app.get("/")
def index():
    return render_template_string(HTML, state=get_state(), format_value=format_value)


@app.post("/threshold")
def set_threshold():
    temp_schwelle = float(request.form["temp_schwelle"])
    set_temp_schwelle(temp_schwelle)

    return redirect(url_for("index"))


def run_webserver():
    app.run(host="0.0.0.0", port=8000)
