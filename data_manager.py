import gspread
from flight_search import FlightSearch


class DataManager:

    def __init__(self):
        gc = gspread.oauth()
        sheet = gc.open_by_key('1RWmy1k8ClU3fpJyBIEj0NHWMU9876qWyrY1Hubq6wnE')
        self.worksheet = sheet.worksheet("prices")
        self.data = self.worksheet.get()

        self.destination_data = []
        self.destination_data = self.get_destination_data()

    def update_iata_codes(self):
        flight_search = FlightSearch()
        for city in self.data:
            if city[1] == '':
                iata_code = flight_search.get_iata_code_by_city_name(city[0])
                city[1] = iata_code
        self.worksheet.update('A1', self.data)

    def get_destination_data(self):
        destination_data = [[city[1], city[2]] for city in self.data if city[1] != "IATA Code"]
        return destination_data


