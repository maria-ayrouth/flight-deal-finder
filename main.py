from pprint import pprint  # formatted
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

# create object from classes
datamanager = DataManager()
flightsearch = FlightSearch()
notificationmanager = NotificationManager()

# use func from classes
sheet_data = datamanager.get_data()  # list of dict

if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch

    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    datamanager.data = sheet_data
    datamanager.update_code()

# search for cheapest flight:
ORIGIN_CITY_IATA = "LON"  # from london for example

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for dest in sheet_data:
    flight = flightsearch.check_flights(ORIGIN_CITY_IATA,
                                        dest['iataCode'],
                                        from_time=tomorrow,
                                        to_time=six_month_from_today)

    if flight is None:
        continue
    else:
      if  flight.price < dest["lowestPrice"] :

         msg=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to" \
            f" {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

         if flight.stop_overs > 0:
            msg += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

         #notificationmanager.send_sms(message=msg)

         # send emails

         users=datamanager.get_emails()
         emails = [row["email"] for row in users]
         link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

         notificationmanager.send_emails(emails, msg, link)

