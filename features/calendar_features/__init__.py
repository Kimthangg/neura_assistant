# Import all calendar-related features
from .create_calendar import *
from .get_calendar import *
from .delete_calendar import *
from .update_calendar import *

# Create a map for all calendar features
calendar_features_map = {
    # "normal_message": {
    #     "example": None,
    #     "tools": None,
    #     "extraction_system_message": ""
    # },
    "create_normal_event": {
        "handler_message": create_event_api,
        "example": create_event_example,
        "tools": tool_create_event,
        "extraction_system_message": system_prompt_create_event,
    },
    "get_freetime": {
        "handler_message": get_free_time_api,
        "example": get_free_time_example,
        "tools": tool_get_event,
        "extraction_system_message": system_prompt_get_event
    },
    "get_multi_calendar": {
        "handler_message": get_multi_calendar_api,
        "example": get_multi_calendar_example,
        "tools": tool_get_event,
        "extraction_system_message": system_prompt_get_event
    },
    "update_event": {
        "handler_message": update_event_api,
        "example": update_event_example,
        "tools": tool_update_event,
        "extraction_system_message": system_prompt_update_event
    },
    "delete_event": {
        "handler_message": delete_event_api,
        "example": delete_event_example,
        "tools": tool_delete_event,
        "extraction_system_message": system_prompt_delete_event
    }
}

