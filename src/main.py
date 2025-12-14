from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.api.routers import pcb_defect_router, log_router

# from src.services.download_model import download_model
# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await download_model()
#     yield
# для swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Detection and classification of PCB defects on production lines",
        version="1.0.1",
        description="This is a Swagger (OpenAPI) application schema for detecting and classifying PCB defects",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI()
app.openapi = custom_openapi

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pcb_defect_router.router)
app.include_router(log_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1")