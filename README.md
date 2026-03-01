# Weather API Frontend

A modern web-based frontend application built with Flask to display weather information. Users select from a dropdown list of cities and click a submit button to fetch real-time weather data from a FastAPI backend connected to OpenWeatherMap.

## Features

- **Modern Web UI**: Clean, responsive interface with gradient design
- **City Dropdown**: Select from 4 major cities (New York, London, Tokyo, Paris)
- **Submit Button**: Fetch weather data from backend API
- **Real-time Weather Display**: Shows temperature, description, humidity, and wind speed
- **Error Handling**: Connection errors and timeouts are handled gracefully
- **Async Loading**: Non-blocking UI updates with loading spinner
- **Docker Support**: Production-ready Docker configuration

## Requirements

- Python 3.7+
- Flask 3.0.0
- requests 2.31.0
- Docker (optional, for containerized deployment)

## Installation

### Prerequisites

Before running the frontend, ensure the backend API is running:
```bash
cd C:\Users\henri\source\repos\WeatherApiBackend
python weather_app.py
```

The backend will be available at `http://127.0.0.1:8000`

### Local Setup

1. Clone/navigate to the frontend directory:
```bash
cd C:\Users\henri\source\repos\WeatherApiFrontend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask application:
```bash
python flask_app.py
```

The frontend will be available at `http://localhost:5000`

## Configuring Backend URL

The frontend communicates with the backend API. To configure the backend URL:

1. Open [flask_app.py](flask_app.py#L7)
2. Modify the `BACKEND_URL` variable:

```python
# Default: backend on same machine
BACKEND_URL = "http://127.0.0.1:8000"

# For remote backend, update to:
BACKEND_URL = "http://your-backend-server.com:8000"
```

3. Save and restart the Flask application

## Dropdown Options

The frontend supports the following 4 cities:

| City | Region |
|------|--------|
| New York | North America |
| London | Europe |
| Tokyo | Asia |
| Paris | Europe |

Cities are dynamically loaded from the backend via the `/api/cities` endpoint.

## How to Run Locally

### Method 1: Direct Python Execution

**Terminal 1 - Start the backend:**
```bash
cd C:\Users\henri\source\repos\WeatherApiBackend
python weather_app.py
```

**Terminal 2 - Start the frontend:**
```bash
cd C:\Users\henri\source\repos\WeatherApiFrontend
python flask_app.py
```

Access the app at: `http://localhost:5000`

### Method 2: Docker Container

1. Build the Docker image:
```bash
docker build -t weather-frontend .
```

2. Run the container:
```bash
docker run -p 5000:5000 --env BACKEND_URL=http://host.docker.internal:8000 weather-frontend
```

Access the app at: `http://localhost:5000`

## Expected UI Layout

### Desktop View
```
┌─────────────────────────────────────────┐
│         🌤️ Weather App                   │
├─────────────────────────────────────────┤
│                                          │
│  Select City:                            │
│  ┌──────────────────────────────────┐   │
│  │ New York                    ▼    │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │    Get Weather     [searching]   │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ✓ Weather data loaded successfully     │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  City:          New York         │   │
│  │  Temperature:   15.3°C           │   │
│  │  Description:   Cloudy           │   │
│  │  Humidity:      65%              │   │
│  │  Wind Speed:    3.2 m/s          │   │
│  └──────────────────────────────────┘   │
│                                          │
└─────────────────────────────────────────┘
```

## Screenshots

### Application Home Screen
- Purple gradient background
- Centered white container
- Title: "🌤️ Weather App"
- City selection dropdown pre-populated with 4 cities
- Large "Get Weather" button

### Weather Result Display
After selecting a city and clicking the button:
- Loading state with spinner animation
- Success message in green box
- Weather details displayed in a card format:
  - City name
  - Temperature in Celsius
  - Weather description
  - Humidity percentage
  - Wind speed in m/s

### Error States
- Red alert box for connection errors
- Clear error messages for missing cities
- "Please select a city" validation

## API Endpoints

### Frontend Endpoints

**GET** `/` - Serves the main HTML page

**GET** `/api/weather?city=<city_name>` - Proxy endpoint to get weather
- Query Parameters: `city` (required)
- Response: JSON weather data

**GET** `/api/cities` - Get available cities
- Response: `{"cities": ["New York", "London", "Tokyo", "Paris"]}`

### Backend Integration

The frontend acts as a proxy to the FastAPI backend:

**Backend Endpoint:**
```
GET http://127.0.0.1:8000/weather?location=<city_name>&include_extra=true
```

**Sample Response:**
```json
{
  "city": "New York",
  "temperature": "15.3°C",
  "description": "Cloudy",
  "humidity": "65%",
  "wind_speed": "3.2 m/s"
}
```

## Project Structure

```
WeatherApiFrontend/
├── flask_app.py              # Main Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── README.md                 # This file
└── templates/
    └── index.html            # Web UI template
```

## Application Flow

1. User opens `http://localhost:5000` in browser
2. Page loads and fetches available cities from `/api/cities`
3. Cities populate in dropdown menu
4. User selects a city from dropdown
5. User clicks "Get Weather" button
6. Frontend shows loading spinner
7. Frontend calls `/api/weather?city=<selected_city>`
8. Backend proxies request to OpenWeatherMap API
9. Weather data displayed in formatted card
10. Success message shown in green box

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot connect to backend" | Ensure backend API is running on `http://127.0.0.1:8000` |
| Dropdown is empty | Check backend `/api/cities` endpoint is responding |
| "City not found" error | Verify city name spelling and exists in OpenWeatherMap database |
| Port 5000 already in use | Change `app.run(port=5001)` in flask_app.py |
| Docker connection errors | Use `host.docker.internal` for localhost references on Windows |

## Notes

- The backend requires an active internet connection to fetch data from OpenWeatherMap
- Port 5000 is used by default for the Flask server
- CORS is not explicitly configured; for cross-origin requests, add Flask-CORS
- The application uses synchronous requests; for high traffic, consider async versions

## Deployment

For production deployment:

1. Use a production WSGI server (gunicorn, waitress)
2. Set `debug=False` in flask_app.py
3. Configure environment variables for backend URL
4. Use Docker for containerized deployment
5. Set up reverse proxy (nginx) for load balancing
