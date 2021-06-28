from app.db.models import RetailerInfo
from app.db.models import User
from app.db.models import ConsolePreference
from playhouse.shortcuts import model_to_dict
from playhouse.shortcuts import dict_to_model

def get_user_by_id(user_id):
    user = User.get_by_id(user_id)
    if not user:
        raise Exception()
        
    return user

def get_retailer_info_by_user_id(user_id = None, user = None):
    if not user_id and not user:
        raise Exception()
    elif not user:
        user = get_user_by_id(user_id)
    elif not user_id:
        user_id = user.id
    return [info for info in user.retailer_info]
    
def get_console_preferences_by_id(retailer_info_id: int = None, retailer_info: RetailerInfo = None) -> list[ConsolePreference]:
    if not retailer_info_id and not retailer_info:
        raise Exception()
    elif not retailer_info:
        retailer_info = get_retailer_info_by_user_id(retailer_info_id)
    elif not retailer_info_id:
        retailer_info_id = retailer_info.id
    return [preference for preference in retailer_info.console_preferences]

def get_aggregate_user_by_id(user_id):
    user = get_user_by_id(user_id)
    retailer_info = get_retailer_info_by_user_id(user)
    payload = model_to_dict(user)
    payload["retailers"] = model_to_dict(retailer_info)
    for retailer in payload["retailers"]:
        console_preferences = get_console_preferences_by_id(retailer_info)
        retailer["console_preferences"] = model_to_dict(console_preferences)
    del payload["password"]
    return payload
