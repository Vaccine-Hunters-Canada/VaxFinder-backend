from dataclasses import dataclass, field
import json

class MalformedAppointmentFile(Exception):
    pass

@dataclass
class Date:
    """Stores day and month as integers; months are 1-12."""
    day: int
    month: int

@dataclass
class Region:
    line1: str = ""
    postal: str = ""
    city: str = ""
    province: str = ""
    line2: str = ""

@dataclass
class VaxRequirements:
    minimumAge: int = 0
    maximumAge: int = 0
    regions: list = field(default_factory=list) #list of Region objects, probably just with postal codes specified
    tags: list = field(default_factory=list)  # List of strings, specifying elgibility as tags (eg, "indigenous", "cancer")
    requiredTags: list = field(default_factory=list) # Same as above, for necessary requirements


class VaxAppointment():
    PFIZER = 0
    MODERNA = 1
    ASTRAZENECA = 2
    JOHNSON = 3
    NOVAVAX = 4
    codes = {"PF": PFIZER, "MD": MODERNA, "AZ": ASTRAZENECA, "JJ": JOHNSON,
            "NV": NOVAVAX}

    def __init__(self, locationName: str, locationAddress: Region, locationVax: list,
                 locationRequirements: VaxRequirements):
        '''

        :param locationName: Name of the location.
        :param locationAddress: Address of location as a Region object, with all values filled out.
        :param locationVax: Vaccine being carried; a list of integers (specified by VaxAppointment.[VACCINE])
        :param locationRequirements: VaxRequirements object, specifying requirements to be elgible for the appointment.
        '''
        self.name = locationName
        self.address = locationAddress
        self.vaccines = locationVax
        self.requirements = locationRequirements

    @classmethod
    def from_json(cls, file):
        '''
        :param file: File object with JSON data.
        :return: VaxAppointment object
        '''
        appointment = json.loads(file.read())
        try:
            name = appointment["name"]
            vaccines = [cls.codes[vaccine] for vaccine in appointment["vaccines"]]
            date = Date(appointment["day"], appointment["month"])
            if (not 0 < date.month < 13) or (not 0 < date.day < 31):
                raise MalformedAppointmentFile("Invalid date provided")
            req = appointment["requirements"]
            regions = [Region(postal=code) for code in req["postalCodes"]]
            requirements = VaxRequirements(req["minimumAge"], req["maximumAge"], regions, req["tags"],
                                           req["requiredTags"])
            loc = appointment["location"]
            location = Region(loc["line1"], loc["postal"], loc["city"], loc["province"], loc["line2"])
            return cls(name, location, vaccines, requirements)
        except IndexError:
            raise MalformedAppointmentFile("Attribute missing from appointment data")