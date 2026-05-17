import json
import requests

def flight_search_tool(source: str, destination: str) -> str:
    """Searches for flights based on source and destination cities. Returns available options sorted by price."""
    try:
        with open("data/flights.json", "r") as f:
            flights = json.load(f)
        filtered = [f for f in flights if f['source'].lower() == source.lower() and f['destination'].lower() == destination.lower()]
        if not filtered:
            return f"No flights found from {source} to {destination}."
        return json.dumps(sorted(filtered, key=lambda x: x['price'])[:3])
    except Exception as e:
        return f"Error: {str(e)}"

def hotel_recommendation_tool(city: str) -> str:
    """Recommends hotels in a specific city, sorted by highest rating."""
    try:
        with open("data/hotels.json", "r") as f:
            hotels = json.load(f)
        filtered = [h for h in hotels if h['city'].lower() == city.lower()]
        if not filtered:
            return f"No hotels found in {city}."
        return json.dumps(sorted(filtered, key=lambda x: x['rating'], reverse=True)[:3])
    except Exception as e:
        return f"Error: {str(e)}"

def places_discovery_tool(city: str) -> str:
    """Finds tourist attractions, points of interest, and beaches for a specific city."""
    try:
        with open("data/places.json", "r") as f:
            places = json.load(f)
        filtered = [p for p in places if p['city'].lower() == city.lower()]
        return json.dumps(filtered) if filtered else f"No points of interest found for {city}."
    except Exception as e:
        return f"Error: {str(e)}"

def weather_lookup_tool(latitude: float, longitude: float) -> str:
    """Fetches a 3-day weather forecast using latitude and longitude coordinates."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max&timezone=auto"
    try:
        response = requests.get(url, timeout=10)
        return json.dumps(response.json().get("daily", {})) if response.status_code == 200 else "Weather unavailable."
    except Exception as e:
        return f"Weather API error: {str(e)}"

def budget_estimation_tool(flight_cost: float, hotel_cost_per_night: float, total_days: int, daily_allowance: float = 2500) -> str:
    """Calculates total estimated trip costs covering flights, accommodations, and local food/travel expenses."""
    try:
        total_hotel = float(hotel_cost_per_night) * int(total_days)
        total_local = float(daily_allowance) * int(total_days)
        return json.dumps({
            "Flight Cost": flight_cost,
            "Total Accommodation Cost": total_hotel,
            "Estimated Food & Local Travel": total_local,
            "Total Estimated Cost": flight_cost + total_hotel + total_local
        })
    except Exception as e:
        return f"Error: {str(e)}"

# Define the exact schemas OpenAI needs to read these functions as tools
openai_tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "flight_search_tool",
            "description": "Searches for flights between source and destination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "destination": {"type": "string"}
                },
                "required": ["source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hotel_recommendation_tool",
            "description": "Recommends hotels in a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "places_discovery_tool",
            "description": "Finds tourist spots in a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weather_lookup_tool",
            "description": "Gets weather data using latitude and longitude coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "budget_estimation_tool",
            "description": "Calculates final total costs for the trip.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_cost": {"type": "number"},
                    "hotel_cost_per_night": {"type": "number"},
                    "total_days": {"type": "integer"},
                    "daily_allowance": {"type": "number"}
                },
                "required": ["flight_cost", "hotel_cost_per_night", "total_days"]
            }
        }
    }
]

# Simple execution mapping dictionary
tools_map = {
    "flight_search_tool": flight_search_tool,
    "hotel_recommendation_tool": hotel_recommendation_tool,
    "places_discovery_tool": places_discovery_tool,
    "weather_lookup_tool": weather_lookup_tool,
    "budget_estimation_tool": budget_estimation_tool
}