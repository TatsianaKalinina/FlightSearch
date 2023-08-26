from flight_data import FlightData
import requests
import os


IATA_API_KEY = os.environ['IATA_API_KEY']
KIWI_API_KEY = os.environ['KIWI_API_KEY']


class FlightSearch:

    def get_iata_code_by_city_name(self, city_name):
        kiwi_api_endpoint = "https://api.tequila.kiwi.com/locations/query"
        kiwi_api_params = {
            "api_key": KIWI_API_KEY,
            "term": city_name,
            "locale": "en-US",
            "location_types": "city",
            "limit": 1
        }
        kiwi_api_headers = {
            "apikey": KIWI_API_KEY,
            "accept": "application/json"
        }
        response = requests.get(url=kiwi_api_endpoint, headers=kiwi_api_headers, params=kiwi_api_params)
        response.raise_for_status()

        data = response.json()
        airport_iata_code = data["locations"][0]["code"]

        return airport_iata_code

    def get_flight_data(self, fly_from_code, fly_to_code, date_from, date_to):
        kiwi_api_endppoint = "https://api.tequila.kiwi.com/v2/search"
        kiwi_api_params = {
            "fly_from": fly_from_code,
            "fly_to": fly_to_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "selected_cabins": "M",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "EUR",
            "max_stopovers": 0,
            "sort": "price",
            "limit": 1,
            "vehicle_type": "aircraft"

        }
        kiwi_api_headers = {
            "apikey": KIWI_API_KEY,
            "accept": "application/json"
        }

        response = requests.get(url=kiwi_api_endppoint, params=kiwi_api_params, headers=kiwi_api_headers)
        response.raise_for_status()

        try:
            data = response.json()
        except IndexError:
            print(f"No flights found for {fly_to_code}.")
            return None

        date_from = data["data"][0]["route"][0]["local_departure"].split("T")[0]
        date_to = data["data"][0]["route"][1]["local_departure"].split("T")[0]
        city_from = data["data"][0]["route"][0]["cityFrom"]
        city_to = data["data"][0]["route"][0]["cityTo"]
        airport_from = data["data"][0]["route"][0]["flyFrom"]
        airport_to = data["data"][0]["route"][0]["flyTo"]
        price = data["data"][0]["price"]

        flight_data = FlightData(
            fly_from_city=city_from,
            fly_from_airport=airport_from,
            fly_to_city=city_to,
            fly_to_airport=airport_to,
            price=price,
            date_from=date_from,
            date_to=date_to
        )
        # print(f"{flight_data.fly_to}: €{flight_data.price}")

        return flight_data
