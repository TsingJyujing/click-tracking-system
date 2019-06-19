# Interface Documentation

## Jump To Page

### Function

Redirect to the page by http 302 response, page is found by the key given, revert to MongoDB ObjectId, then search details in MongoDB.

### Urls

- `/j`
- `/api/redirect`

### Parameters

|Name|Value Example|Necessary|Method|Comment|
|-|-|-|-|-|
|k|XQJAcQAnn6xSCU87|yes|GET|-|

## Create a Link

### Function

Create a link and return the key.

### Urls

- `/api/create`

### Parameters

|Name|Value Example|Necessary|Method|Comment|
|-|-|-|-|-|
|url|https://www.google.com/|yes|POST|-|
|token|5d02407100279fac52094f3b|yes*|GET/POST|-|

## Disable a Link

### Function

Disable to visit some link.

### Urls

- `/api/disable`


### Parameters
|Name|Value Example|Necessary|Comment|
|-|-|-|-|
|key|XQJAcQAnn6xSCU87|yes|POST|-|
|token|5d02407100279fac52094f3b|yes*|GET/POST|-|

### Response Examples

#### While Success
```json
{
    "status": "success"
}
```

#### While Something Wrong
```json
{
    "status": "error",
    "error_info": "Executed successfully but didn't modify anything.",
    "trace_back": "Traceback (most recent call last):\n  File \"/Users/st22130/PycharmProjects/click-tracking-system/utility/http_response.py\", line 123, in wrapper\n    return get_json_response(func(request))\n  File \"/Users/st22130/PycharmProjects/click-tracking-system/api/views.py\", line 139, in enable_link\n    raise Exception(\"Executed successfully but didn't modify anything.\")\nException: Executed successfully but didn't modify anything.\n"
}
```

## Enable a Link

### Function

To set some key is valid for visiting and redirecting.

### Urls

- `/api/disable`

### Parameters
|Name|Value Example|Necessary|Comment|
|-|-|-|-|
|key|XQJAcQAnn6xSCU87|yes|POST|-|
|token|5d02407100279fac52094f3b|yes*|GET/POST|-|

### Response Examples

#### While Success
```json
{
    "status": "success"
}
```

#### While Something Wrong
```json
{
    "status": "error",
    "error_info": "Executed successfully but didn't modify anything.",
    "trace_back": "Traceback (most recent call last):\n  File \"/Users/st22130/PycharmProjects/click-tracking-system/utility/http_response.py\", line 123, in wrapper\n    return get_json_response(func(request))\n  File \"/Users/st22130/PycharmProjects/click-tracking-system/api/views.py\", line 139, in enable_link\n    raise Exception(\"Executed successfully but didn't modify anything.\")\nException: Executed successfully but didn't modify anything.\n"
}
```
## Get Link Details

### Function

Get details (redirect link and key-value pairs data) in JSON format.

### Urls
- `/api/detail`

### Parameters

|Name|Value Example|Necessary|Method|Comment|
|-|-|-|-|-|
|key|XQJAcQAnn6xSCU87|yes|GET|-|
|token|5d02407100279fac52094f3b|yes*|GET/POST|-|

### Response Example

```json
{
    "url": "https://www.google.com/",
    "data": {
        "test": 1
    },
    "valid": false,
    "key": "XQJAcQAnn6xSCU87",
    "status": "success"
}
```

## About 

- [*] Token is not necessary if you're login, but you'd like to put django style token in cookies.