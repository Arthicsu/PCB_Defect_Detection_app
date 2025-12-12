from fastapi import APIRouter
from .routers import pcb_defect_router

router = APIRouter()

router.include_router(pcb_defect_router.router)