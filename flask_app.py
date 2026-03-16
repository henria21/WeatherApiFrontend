import logging
import os

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# Backend API configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Cities list
CITIES = ["New York", "London", "Tokyo", "Paris"]


@app.route("/")
def index():
    """Serve the main page"""
    return render_template("index.html", cities=CITIES)


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


@app.route("/api/weather", methods=["GET"])
def get_weather():
    """Proxy endpoint to get weather from backend"""
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    if len(city) > 100:
        return jsonify({"error": "City parameter too long"}), 400

    try:
        # Call the backend API
        response = requests.get(
            f"{BACKEND_URL}/weather",
            params={"location": city, "include_extra": True},
            timeout=5,
        )

        if response.status_code == 200:
            return jsonify(response.json())

        logger.warning("Backend returned %s for city=%s", response.status_code, city)
        return jsonify({"error": response.json().get("detail", "Error fetching weather")}), response.status_code

    except requests.exceptions.Timeout:
        logger.error("Backend timeout for city=%s", city)
        return jsonify({"error": "Weather service timed out"}), 503

    except requests.exceptions.RequestException as e:
        logger.error("Backend request failed for city=%s: %s", city, e)
        return jsonify({"error": "Weather service unavailable"}), 503


@app.route("/api/cities", methods=["GET"])
def get_cities():
    """Get list of available cities"""
    return jsonify({"cities": CITIES})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "127.0.0.1")
    app.run(debug=debug, host=host, port=port)
