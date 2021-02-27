from utils.intent import IAPIntent
from utils import intent_utils
import requests
from tts import tts


class WeatherAtPlaceIntent(IAPIntent):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.setting = intent_utils.get_settings(__file__)
        self.global_settings = intent_utils.get_global_setting()

    def get_openweathermap(self, city):
        return requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.setting['api_token']}&lang={self.global_settings['language_short']}&units={self.global_settings['units']}")

    def intent_detected(self, wit_result):
        locations = intent_utils.get_locations(wit_result)
        location_one = locations[0]["body"]
        weather = self.get_openweathermap(location_one).json()
        print(weather)
        tts.say(
            f"in {location_one} ist es gerade {weather['weather'][0]['description']} mit einer temperatur von {round(weather['main']['temp'])}°. Die minimale bzw. maximale Temperatur beträgt {round(weather['main']['temp_min'])} bzw. {round(weather['main']['temp_max'])}°")


def create_intent():
    return WeatherAtPlaceIntent()
