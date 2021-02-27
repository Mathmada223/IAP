from utils.intent import IAPIntent
from utils import intent_utils
from tts import tts
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz


class TimeAtPlaceIntent(IAPIntent):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.geolocator = Nominatim(user_agent="geoapiExercises")
        self.timezonefinder = TimezoneFinder()

    def intent_detected(self, wit_result):
        locations = intent_utils.get_locations(wit_result)
        location_one = locations[0]["body"]

        location_geocoded = self.geolocator.geocode(location_one)

        time_zone = pytz.timezone(
            self.timezonefinder.timezone_at(lng=location_geocoded.longitude, lat=location_geocoded.latitude))
        time = datetime.now(time_zone)

        tts.say(f"Die Uhrzeit in {location_one} ist {time.strftime('%H:%M')}")


def create_intent():
    return TimeAtPlaceIntent()
