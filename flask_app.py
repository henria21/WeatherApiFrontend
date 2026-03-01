from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:8000"

# Cities list
CITIES = ["New York", "London", "Tokyo", "Paris"]

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html', cities=CITIES)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Proxy endpoint to get weather from backend"""
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    
    try:
        # Call the backend API
        response = requests.get(
            f"{BACKEND_URL}/weather",
            params={"location": city, "include_extra": True},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.json().get("detail", "Error fetching weather")}), response.status_code
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Connection error: {str(e)}"}), 503

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of available cities"""
    return jsonify({"cities": CITIES})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
