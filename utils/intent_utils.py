import pathlib
import json
import os.path as path


def get_entities(wit_response, entity_name):
    return wit_response["entities"][entity_name]


def get_locations(wit_response):
    return get_entities(wit_response, "wit$location:location")


def get_wikipedia_search_queries(wit_reponse):
    return get_entities(wit_reponse, "wit$wikipedia_search_query:wikipedia_search_query")

def get_settings(file):
    with open(path.join(pathlib.Path(file).parent.absolute(), "settings.json"), "r") as f:
        return json.load(f)

def get_global_setting():
    with open(path.join(pathlib.Path(__file__).parent.absolute(), "options.json"), "r") as f:
        return json.load(f)