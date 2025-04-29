# traffic_light_system.py
import requests
import time

class TrafficLight:
    def __init__(self, location):
        self.location = location
        self.state = "RED"
        self.green_time = 30
        self.yellow_time = 5
        self.red_time = 30

    def update_state(self):
        if self.state == "RED":
            self.state = "GREEN"
        elif self.state == "GREEN":
            self.state = "YELLOW"
        elif self.state == "YELLOW":
            self.state = "RED"

    def get_current_duration(self):
        if self.state == "GREEN":
            return self.green_time
        elif self.state == "YELLOW":
            return self.yellow_time
        else:
            return self.red_time

class RealTimeData:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_traffic_data(self, origin, destination):
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "departure_time": "now",
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            try:
                traffic_duration = data["rows"][0]["elements"][0]["duration_in_traffic"]["value"]
                return traffic_duration
            except KeyError:
                return None
        else:
            return None

class TrafficLightSystem:
    def __init__(self, locations, api_key):
        self.lights = [TrafficLight(loc) for loc in locations]
        self.data_fetcher = RealTimeData(api_key)

    def adjust_light_timings(self):
        for light in self.lights:
            origin = light.location
            destination = light.location
            traffic_time = self.data_fetcher.fetch_traffic_data(origin, destination)

            if traffic_time is not None:
                if traffic_time > 600:
                    light.green_time = 45
                elif traffic_time < 300:
                    light.green_time = 20
                else:
                    light.green_time = 30
            else:
                light.green_time = 30

# NOTE: We DO NOT have a "run" here — just class definitions.
# (No "if __name__ == '__main__'" section here.)
