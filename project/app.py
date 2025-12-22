import query
from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@dataclass
class DKIMResponse:
    status: str
    code: int
    keys_found: int
    domain: str
    data: list[dict]


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/{domain}")
async def read_api_data(domain: str):
    data = []
    try:
        results = await query.gather_dns_results(domain)
        for result in results:
            if result:
                data.append(result)
        keys_found = len(data)
        response = DKIMResponse("success", 200, keys_found, domain, data)
        return response
    except Exception as e:
        print(f"ERROR: {e}")
        response = DKIMResponse("fail", 500, 0, domain, data)
        return response
