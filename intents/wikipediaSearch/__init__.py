from utils.intent import IAPIntent
from utils import intent_utils
import wikipedia
from tts import tts

class WikipediaSearchIntent(IAPIntent):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.global_settings = intent_utils.get_global_setting()
        wikipedia.set_lang(self.global_settings["language_short"])

    def intent_detected(self, wit_result):
        search = intent_utils.get_wikipedia_search_queries(wit_result)[0]["body"]
        tts.say(wikipedia.summary(search, sentences=1))

def create_intent():
    return WikipediaSearchIntent()