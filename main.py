from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.destination_data
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "BER"

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.get_flight_data(
        ORIGIN_CITY_IATA,
        destination[0],
        date_from=tomorrow,
        date_to=six_month_from_today
    )
    if flight.price < int(destination[1]):
        # print(f"Low price alert! Only €{flight.price} to fly from {flight.fly_from}-{flight.fly_from_airport} to {flight.fly_to}-{flight.fly_to_airport}, from {flight.date_from} to {flight.date_to}.")
        notification_manager.send_sms(
            sms=f"Low price alert! Only €{flight.price} to fly from {flight.fly_from}-{flight.fly_from_airport} to {flight.fly_to}-{flight.fly_to_airport}, from {flight.date_from} to {flight.date_to}."
        )
