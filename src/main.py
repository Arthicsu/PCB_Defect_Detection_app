from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.api.routers import pcb_defect_router, log_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pcb_defect_router.router)
app.include_router(log_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1")