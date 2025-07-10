import logging
import aiohttp
from datetime import datetime, timedelta

API_FOOTBALL_KEY = "6a166f5705742c52edbcc1c4f1115d5e"
HEADERS = {"X-RapidAPI-Key": API_FOOTBALL_KEY}

# Logging
logging.basicConfig(level=logging.INFO)

async def fetch_data(url, params=None):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        try:
            async with session.get(url, params=params) as response:
                logging.info(f"Requesting: {url} with params {params}")
                data = await response.json()
                logging.info(f"Response: {data}")
                return data
        except Exception as e:
            logging.error(f"API error: {e}")
            return None

async def get_live_matches(sport):
    if sport == "football":
        url = "https://v3.football.api-sports.io/fixtures"
        params = {"live": "all"}
    elif sport == "tennis":
        url = "https://v1.tennis.api-sports.io/matches"
        params = {"live": "all"}
    else:
        return []

    data = await fetch_data(url, params)
    if not data or "response" not in data:
        logging.warning(f"No data or empty response for {sport}")
        return []

    return data["response"]

async def get_upcoming_matches(sport):
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    if sport == "football":
        url = "https://v3.football.api-sports.io/fixtures"
        params = {
            "date": today.strftime("%Y-%m-%d")
        }
    elif sport == "tennis":
        url = "https://v1.tennis.api-sports.io/matches"
        params = {
            "date": today.strftime("%Y-%m-%d")
        }
    else:
        return []

    data = await fetch_data(url, params)
    if not data or "response" not in data:
        logging.warning(f"No upcoming data for {sport}")
        return []

    return data["response"]
