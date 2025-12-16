import query
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the templates directory
templates = Jinja2Templates(directory="templates")

success_response = {
    "status": "success",
    "code": 200,
    "dkim_keys_found": None,
    "message": "hello world",
    "domain": "kalf.me",
    "data": [],
    "meta": {"timestamp": "2023-10-27T10:00:00Z", "request_id": "req_8923749823"},
}


class DKIMResponse:
    def __init__(self, status: str, code: int, keys_found, domain: str, data: list):
        self.status = status
        self.code = code
        self.keys_found = keys_found
        self.domain = domain
        self.data = data


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/{domain}")
async def read_api_data(domain: str):
    try:
        result = await query.bulk_lookup_resolver(domain)
        data = []
        for x in result:
            if x:
                data.append(x)

                # for y, z in x.items():
                #     print(f"{y}:{z}")
        keys_found = len(data)
        response = DKIMResponse("success", 200, keys_found, domain, data)
        return response
    except Exception as e:
        return e


response1 = {
    "status": "success",
    "code": 200,
    "dkim_keys_found": 5,
    "message": "hello world",
    "domain": "kalf.me",
    "data": [
        {
            "selector": "fm1",
            "record_type": "CNAME",
            "original_query": "fm1._domainkey.kalf.me.",
            "cname_target": "fm1.kalf.me.dkim.fmhosted.com.",
            "records": [
                "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4zlu37P..."
            ],
        },
        {
            "selector": "default",
            "record_type": "TXT",
            "original_query": "default._domainkey.kalf.me.",
            "cname_target": None,
            "records": [
                "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4zlu37P..."
            ],
        },
    ],
    "meta": {"timestamp": "2023-10-27T10:00:00Z", "request_id": "req_8923749823"},
}


# # Route for a JSON API endpoint
# @app.route("/api/v1/dkim-key-search")
# async def api_hello():
#     logger.info("Handling request to the root endpoint")

#     results = await query.bulk_lookup_resolver()
#     logger.info(results)

#     message = {
#         "message": "Hello World from Flask API!",
#         "message": [
#             {"one": "Hello World from Flask API!", "two": "Hello World from Flask API!"}
#         ],
#     }
#     return jsonify(message)
