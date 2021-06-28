from _pytest.config import exceptions
from app.db import store
from app.db.models import User
import pytest 



def test_get_user_by_id(mocker):
    user_mock = mocker.Mock() 

    mocker.patch("app.db.store.User.get_by_id", return_value = user_mock)

    #mocker.patch("app.db.store.model_to_dict", return_value = {"password":"sql"})

    results = store.get_user_by_id(2258)

    assert results == user_mock

def test_get_user_by_id_no_user(mocker):
    
    mocker.patch("app.db.store.User.get_by_id", return_value = None)

    with pytest.raises(Exception):
        results = store.get_user_by_id(2258)

