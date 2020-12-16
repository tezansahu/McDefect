# == RESTful API Server for McDefect Solutions ==

"""
This is the RESTful API for McDefect Solutions. It has been developed using FastAPI & documented using Pycco.
It allows for the following requests being made:

1. **GET /** - Hits the API root
2. **POST /defect** - Upload an image for detection of defects
3. **POST /classify** - Upload an image for categorization of defects

*Currently, the app uses only one model for defect detection & another for defect categorization. 
In future, we plan to implement API Key based authentication to allow multiple partners to use the models related to their specific use cases separately & seamlessly.*
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from routers import detect, classify


app = FastAPI()

# **Cross Origin Resource Sharing** has been enabled across all hosts (only for demonstration purposes)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# === GET / ===

"""
This is the Root of the RESTful API for McDefect Solutions
"""
@app.get("/")
def get_root():
    
    return "This is the RESTful API for McDefect Solutions"


# === POST /defect ===

"""
This is the mounting position for all API endpoints related to Defect Detection. Its implementation(s) can be found in [routers/detect.py](./routers/detect.html)
"""
app.include_router(
    detect.router,
    prefix="/detect",
    tags=["defect detection"],
    responses={404: {"description": "Not found"}},
)


# === POST /classify ===

"""
This is the mounting position for all API endpoints related to Defect Classification. Its implementation(s) can be found in [routers/classify.py](./routers/classify.html)
"""
app.include_router(
    classify.router,
    prefix="/classify",
    tags=["defect classification"],
    responses={404: {"description": "Not found"}},
)

# === Interactive API Documentation ===

"""
FastAPI automatically creates an interactive API documentation for the API server being developed. Here, we set some of the details of this documentation page.
The docs can be obtained by hitting the **GET /doc** endpoint. For example, if the server is deployed at `http://localhost:8000`, one can find the interactive
documentation at `http://localhost:8000/doc`
"""

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