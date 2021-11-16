import requests
from flight_data import FlightData
from pprint import pprint

API_KEY = "YOUR API KEY"
Tequila_EndPoint = "https://tequila-api.kiwi.com"
location_endpoint = f"{Tequila_EndPoint}/locations/query"
search_endpoint = f"{Tequila_EndPoint}/v2/search"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def get_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }
        header = {
            "apikey": API_KEY
        }
        response = requests.get(url=location_endpoint, params=params, headers=header)
        code = response.json()["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": API_KEY}

        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=search_endpoint, params=query, headers=headers)

        try:
            data = response.json()["data"][0]  # first item of the list data
        except IndexError:
            # print(f"No flights found for {destination_city_code}.") # with 0 stop over , now we should verify if we have flight with 1 stop over
            # return None
            query["max_stopovers"] = 1
            response = requests.get(url=search_endpoint, params=query, headers=headers)
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            else:
                flightdata = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
            print(f"{flightdata.destination_city}: £{flightdata.price}")
            return flightdata


        else:
            flightdata = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
        print(f"{flightdata.destination_city}: £{flightdata.price}")
        return flightdata
