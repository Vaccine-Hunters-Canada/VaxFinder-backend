from flask_restful import Resource, reqparse
from vaxfinder.appointments import Region, MalformedLocation
import vaxfinder.database as database
import json

class Location(Resource):
    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("location", type=dict)
        parser.add_argument("organization", type=int)
        parser.add_argument("phonenumber", type=str)
        parser.add_argument("bookingurl", type=str)
        self.parser = parser

    def get(self):
        return 200

    def post(self):
        data = self.parser.parse_args()
        try:
            region = Region.from_json(json.dumps(data["location"]))
        except (KeyError, MalformedLocation):
            return ("Invalid address provided", 400)
        try:
            name = data['name']
        except KeyError:
            return ("No location name provided", 400)
        organization = data.get("organization")
        booking_url = data.get("bookingurl")
        phone_number = data.get("phonenumber")
        try:
            id = database.add_location(name, region, booking_url, phone_number, organization)
        except database.DBException:
            return ("Invalid data provided", 400)
        return (id, 200)