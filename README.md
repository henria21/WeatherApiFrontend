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

- Python 3.11+
- Flask 3.0.0
- requests 2.31.0
- pytest 8.1.1
- Docker (optional, for containerized deployment)

## Installation

### Prerequisites

Before running the frontend, ensure the backend API is running:

```bash
cd path/to/WeatherApiBackend
python weather_app.py
```

The backend will be available at `http://127.0.0.1:8000`

### Local Setup

1. Clone/navigate to the frontend directory:

```bash
cd path/to/WeatherApiFrontend
```

1. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv/Scripts/activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Run the Flask application:

```bash
python flask_app.py
```

The frontend will be available at `http://localhost:5000`

## Configuration

The application is configured via environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `BACKEND_URL` | `http://127.0.0.1:8000` | URL of the FastAPI backend |
| `PORT` | `5000` | Port for the Flask server |
| `HOST` | `127.0.0.1` | Host to bind the Flask server |
| `FLASK_DEBUG` | `false` | Enable debug mode (`true`/`false`) |

Example:

```bash
BACKEND_URL=http://my-backend:8000 PORT=8080 python flask_app.py
```

## Dropdown Options

The frontend supports the following 4 cities:

| City | Region |
| --- | --- |
| New York | North America |
| London | Europe |
| Tokyo | Asia |
| Paris | Europe |

Cities are dynamically loaded from the backend via the `/api/cities` endpoint.

## How to Run Locally

### Method 1: Direct Python Execution

**Terminal 1 - Start the backend:**

```bash
cd path/to/WeatherApiBackend
python weather_app.py
```

**Terminal 2 - Start the frontend:**

```bash
cd path/to/WeatherApiFrontend
python flask_app.py
```

Access the app at: `http://localhost:5000`

### Method 2: Docker Container

1. Build the Docker image:

```bash
docker build -t weather-frontend .
```

1. Run the container:

```bash
docker run -p 5000:5000 -e BACKEND_URL=http://host.docker.internal:8000 weather-frontend
```

Access the app at: `http://localhost:5000`

## Expected UI Layout

### Desktop View

```text
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

**GET** `/health` - Health check endpoint

**GET** `/api/weather?city=<city_name>` - Proxy endpoint to get weather

- Query Parameters: `city` (required)
- Response: JSON weather data

**GET** `/api/cities` - Get available cities

- Response: `{"cities": ["New York", "London", "Tokyo", "Paris"]}`

### Backend Integration

The frontend acts as a proxy to the FastAPI backend:

**Backend Endpoint:**

```text
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

```text
WeatherApiFrontend/
├── flask_app.py              # Main Flask application
├── weather_frontend.py       # Desktop Tkinter GUI (standalone)
├── test_flask_app.py         # Unit tests
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── README.md                 # This file
└── templates/
    └── index.html            # Web UI template
```

## Running Tests

```bash
pytest test_flask_app.py -v
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
| --- | --- |
| "Cannot connect to backend" | Ensure backend API is running on `http://127.0.0.1:8000` |
| Dropdown is empty | Check backend `/api/cities` endpoint is responding |
| "City not found" error | Verify city name spelling and exists in OpenWeatherMap database |
| Port 5000 already in use | Set `PORT=5001` environment variable |
| Docker connection errors | Use `host.docker.internal` for localhost references on Windows |

## Notes

- The backend requires an active internet connection to fetch data from OpenWeatherMap
- Port 5000 is used by default for the Flask server
- CORS is not explicitly configured; for cross-origin requests, add Flask-CORS
- The application uses synchronous requests; for high traffic, consider async versions

## Deployment

For production deployment:

1. Use a production WSGI server (gunicorn, waitress)
2. Set `FLASK_DEBUG=false` (default)
3. Set `BACKEND_URL` environment variable to your backend address
4. Use Docker for containerized deployment
5. Set up reverse proxy (nginx) for load balancing
