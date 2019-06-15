import json
from base64 import b64decode, b64encode
from datetime import datetime
from bson import ObjectId
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from config import get_mongo_connection, get_kvs, DATA_REDUNDANCY
from service.logging_service import provide
from utility.http_response import on_error_not_found_page, response_json
from utility.token_verify import token_required

__LIMIT_TIME = datetime(2019, 1, 1)
conn = get_mongo_connection()


def b64replace(b64data: str):
    return b64data.replace("/", "-")


def b64revert(b64data: str):
    return b64data.replace("-", "/")


def _convert_oid_to_key(oid: ObjectId) -> str:
    return b64replace(b64encode(bytes.fromhex(str(oid))).decode())


def _convert_key_to_oid(key: str) -> ObjectId:
    """
    Check key statistically to ensure it's valid
    Reduce the pressure of mongodb
    :param key: base64
    :return: object ID
    """
    oid = ObjectId(bytes.hex(b64decode(b64revert(key))))
    # assert oid.generation_time > __LIMIT_TIME, "ID should not earlier than 2019"
    # assert oid.generation_time < (datetime.now() - timedelta(days=1)), "ID should not later than tomorrow"
    return oid


def __get_ip_address(request):
    """
    Get ip address from request
    :param request:
    :return:
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")
    client_ip = ip.split(",")[-1].strip() if ip else ""
    return client_ip


def _extract_info_from_request(request: HttpRequest):
    """
    Extract details from requests
    :param request:
    :return:
    """
    return {
        "headers": request.headers,
        "ip": __get_ip_address(request)
    }


@on_error_not_found_page
def get_redirect_page(request: HttpRequest) -> HttpResponse:
    """
    Redirect to URL by the key given, and insert log asynchronously
    :param request: The django request
    :return:
    """
    _id = _convert_key_to_oid(request.GET["k"])
    res = get_kvs(conn).find_one({"_id": _id})
    assert res is not None, "Can't find URL in database"
    assert res["valid"], "URL is not valid"
    data = _extract_info_from_request(request)
    data["url_id"] = _id
    data["visit_time"] = datetime.now()
    if DATA_REDUNDANCY:
        data["data"] = res["data"]
        data["url"] = res["url"]
    provide(data)
    url = res["url"]

    return redirect(url, permanent=False)


@csrf_exempt
@token_required
@response_json
def create_new_link(request: HttpRequest):
    url_id = get_kvs(conn).insert_one({
        "url": request.POST["url"],
        "data": json.loads(request.POST["data"]),
        "valid": True
    }).inserted_id
    return {
        "id": _convert_oid_to_key(url_id)
    }


@csrf_exempt
@token_required
@response_json
def disable_link(request: HttpRequest):
    modify_result = get_kvs(conn).update_one({
        "_id": _convert_key_to_oid(request.POST["key"])
    }, {
        "$set": {
            "valid": False
        }
    }).modified_count > 0
    if modify_result:
        return {
            "status": "success"
        }
    else:
        raise Exception("Executed successfully but didn't modify anything.")


@csrf_exempt
@token_required
@response_json
def enable_link(request: HttpRequest):
    modify_result = get_kvs(conn).update_one({
        "_id": _convert_key_to_oid(request.POST["key"])
    }, {
        "$set": {
            "valid": True
        }
    }).modified_count > 0
    if modify_result:
        return {
            "status": "success"
        }
    else:
        raise Exception("Executed successfully but didn't modify anything.")


@token_required
@response_json
def basic_information(request: HttpRequest):
    query_result = get_kvs(conn).find_one({"_id": _convert_key_to_oid(request.GET["key"])})
    assert query_result is not None, "Key not exist."
    _id = query_result.pop("_id")
    query_result["key"] = _convert_oid_to_key(_id)
    query_result["status"] = "success"
    return query_result
