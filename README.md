# flight-deal-finder

we create a cheap flight finder by using a combination off different APIs .our program is going to fing amazing flight deals .

first , we have a google sheet which keeps track of the locations that we want to visit and a price cutoff . so we take this data from our google sheet with lots of gifferent locations and their lowest prices and we feed that into a flight search API which is going to search through all of the locations looking for the cheapest flight in the next 6 months .

when it comes up with a hit and it finds a flight that's actually cheaper than our predefined price , then it's going to send that date and price via our Twilio SMS module to our mobile phone  so that we can book it  .
