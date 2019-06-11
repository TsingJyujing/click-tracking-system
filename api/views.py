from base64 import b64decode
from datetime import datetime, timedelta

from bson import ObjectId
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from config import get_mongo_connection, get_kvs, DATA_REDUNDANCY
from service.logging_service import provide

# Create your views here.

__LIMIT_TIME = datetime(2019, 1, 1)
conn = get_mongo_connection()


def check_key(key: str) -> ObjectId:
    """
    Check key statistically to ensure it's valid
    Reduce the pressure of mongodb
    :param key: base64
    :return: object ID
    """
    oid = ObjectId(bytes.hex(b64decode(key)))
    assert oid.generation_time > __LIMIT_TIME, "ID should not earlier than 2019"
    assert oid.generation_time < (datetime.now() - timedelta(days=1)), "ID should not later than tomorrow"
    return oid


# TODO add error processing here
def get_redirect_page(request: HttpRequest) -> HttpResponse:
    """
    Redirect to URL by the key given, and insert log asynchronously
    :param request: The django request
    :return:
    """
    _id = check_key(request.GET["k"])
    res = get_kvs(conn).find_one({"_id": _id})
    assert res is not None, "Can't find URL in database"
    # todo ensure correct
    # todo add more fields like IP
    data = {
        "url_id": _id,
        "visit_time": datetime.now(),
        "headers": request.headers
    }
    if DATA_REDUNDANCY:
        data["data"] = res["data"]
        data["url"] = res["url"]
    provide(data)
    url = res["url"]
    return redirect(url, permanent=False)

# todo these interfaces need authority

# todo add a new link
# todo disable a key
# todo re-enable a key
# todo get basic information
