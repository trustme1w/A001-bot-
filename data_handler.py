import requests
from config import FOOTBALL_API_KEY, TENNIS_API_KEY

class DataHandler:
    def __init__(self):
        self.football_api_key = FOOTBALL_API_KEY
        self.tennis_api_key = TENNIS_API_KEY

    def get_live_football(self):
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {"x-apisports-key": self.football_api_key}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None

    def get_prematch_football(self):
        url = "https://v3.football.api-sports.io/fixtures?next=10"
        headers = {"x-apisports-key": self.football_api_key}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None

    def get_live_tennis(self):
        url = "https://api.the-odds-api.com/v4/sports/tennis/events/?regions=eu&oddsFormat=decimal"
        headers = {"x-apisports-key": self.tennis_api_key}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None

    def get_prematch_tennis(self):
        url = "https://api.the-odds-api.com/v4/sports/tennis/events/?regions=eu&oddsFormat=decimal"
        headers = {"x-apisports-key": self.tennis_api_key}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
