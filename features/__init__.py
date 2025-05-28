from .calendar_features import *
from .gmail_features import *


full_features_map = {
    **calendar_features_map,
    **gmail_features_map
}

def intent_example_dict():
    intent_example = {}
    for key, feature in full_features_map.items():
        if feature.get("example"):
            for example in feature["example"]:
                intent_example[example] = key
    return intent_example

