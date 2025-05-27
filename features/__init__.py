from .create_calendar.handler import *
from .get_calendar.first_calendar.handler import *
from .get_calendar.free_time.handler import *
from .get_calendar.multi_calendar.handler import *
from .update_calendar.handler import *
from .delete_calendar.handler import *
from .normal_message.handler import *

from .create_calendar.example import *
from .get_calendar.first_calendar.example import*
from .get_calendar.free_time.example import *
from .get_calendar.multi_calendar.example import *

from .update_calendar.example import *
from .delete_calendar.example import *
from .normal_message.example import *

from bot.agent_calendar.create_event.datetime_extraction import system_prompt_create_event, tool_create_event
from bot.agent_calendar.get_event.datetime_extraction import system_prompt_get_event, tool_get_event
from bot.agent_calendar.delete_event.datetime_extraction import system_prompt_delete_event, tool_delete_event
from bot.agent_calendar.update_event.datetime_extraction import system_prompt_update_event, tool_update_event

#gmail
from bot.agent_gmail.datetime_extraction import system_prompt_summary_gmail, tool_summary_gmail
from .gmail_features.summarize_emails.handler import *
from .gmail_features.summarize_emails.example import *

calendar_features_map = {
    "normal_message": {
    # "handler_message": chitchat,
    "example": None,
    "tools": None,
    "extraction_system_message":""
    },
    # =============== Agent Calendar Features ===============
    "create_normal_event": {
        "handler_message": create_event_api,
        "example": create_event_example,
        "tools": tool_create_event,
        "extraction_system_message": system_prompt_create_event,
        
    },
    # "get_first_calendar": {
    #     "handler_message": get_first_calendar_api,
    #     "example": get_first_calendar_example,
    #     "tools": tool_get_event,
    #     "extraction_system_message":system_prompt_get_event
    # },
    "get_freetime": {
        "handler_message": get_free_time_api,
        "example": get_free_time_example,
        "tools": tool_get_event,
        "extraction_system_message":system_prompt_get_event
    },
    "get_multi_calendar": {
        "handler_message": get_multi_calendar_api,
        "example": get_multi_calendar_example,
        "tools": tool_get_event,
        "extraction_system_message":system_prompt_get_event
    },
    
    "update_event": {
      "handler_message": update_event_api,
      "example": update_example,
        "tools": tool_update_event,
      "extraction_system_message": system_prompt_update_event
    },
    "delete_event": {
      "handler_message": delete_event_api,
      "example": delete_event_example,
      "tools": tool_delete_event,
      "extraction_system_message": system_prompt_delete_event
    },
    # =============== Agent Gmail Features ===============
    "summary_gmail": {
      "handler_message": get_context_mail_api,
      "example": summary_gmail_example,
      "tools": tool_summary_gmail,
      "extraction_system_message": system_prompt_summary_gmail
    },
    # "search_gmail": {
    #     "handler_message": search_gmail_api,
    #     "example": search_gmail_example,
    #     "tools": None,  # Assuming no specific tool for this feature
    #     "extraction_system_message": ""
    # }
}

def intent_example_dict():
    intent_example = {}
    for key, feature in calendar_features_map.items():
        if feature.get("example"):
            for example in feature["example"]:
                intent_example[example] = key
    return intent_example
