from utils.intent import IAPIntent
from utils import intent_utils
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
from tts import tts


class LocationBetweenPlacesIntent(IAPIntent):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.geolocator = Nominatim(user_agent="geoapiExercises")

    def get_distance(self, lat1, lng1, lat2, lng2):
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lng1)
        lat2 = radians(lat2)
        lon2 = radians(lng2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def intent_detected(self, wit_result):
        locations = intent_utils.get_locations(wit_result)
        location_one, location_two = self.geolocator.geocode(locations[0]["body"]), self.geolocator.geocode(
            locations[1]["body"])
        dist = self.get_distance(location_one.longitude, location_one.latitude, location_two.longitude,
                                 location_two.latitude)
        tts.say(f"{str(location_one).split(',')[0]} ist {round(dist)}km von {str(location_two).split(',')[0]} entfernt")


def create_intent():
    return LocationBetweenPlacesIntent()
