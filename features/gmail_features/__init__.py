# from .search_emails import *
from .summarize_emails import *

# =============== Agent Gmail Features ===============
gmail_features_map = {
    "summarize_emails": {
        "handler_message": summarize_emails_api,
        "example": summarize_emails_example,
        "tools": tool_summarize_emails,
        "extraction_system_message": system_prompt_summarize_emails
    }
    # "search_gmail": {
    #     "handler_message": search_emails_api,
    #     "example": search_emails_example,
    #     "tools": None,  # Assuming no specific tool for this feature
    #     "extraction_system_message": ""
    # }
}