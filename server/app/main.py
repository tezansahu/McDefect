from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from routers import detect, classify

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def get_root():
    return "This is the RESTful API for McDefect Solutions"

app.include_router(
    detect.router,
    prefix="/detect",
    tags=["defect detection"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    classify.router,
    prefix="/classify",
    tags=["defect classification"],
    responses={404: {"description": "Not found"}},
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="McDefect Solutions",
        version="0.0.1",
        description="This is the RESTful API for McDefect Solutions",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi