import requests

sheet_endpoint = "https://api.sheety.co/546c58815188ad78e5e1950cb8125deb/flightDeals/prices"


class DataManager:
    def __init__(self):
        self.data = {}


    def get_data(self):
        response = requests.get(url=sheet_endpoint)
        self.data = response.json()["prices"]  # list of dict
        return self.data

    def update_code(self):
        for city in self.data:
            new_data = {
                "price": {"iataCode": city["iataCode"]}
            }
            response = requests.put(url=f"{sheet_endpoint}/{city['id']}",json=new_data)
            print(response.text)

    def get_emails(self):
        users_endpoint="https://api.sheety.co/546c58815188ad78e5e1950cb8125deb/flightDeals/users"
        response = requests.get(url=users_endpoint)
        data = response.json()
        self.user_data=data["users"]  # list of dict
        return  self.user_data