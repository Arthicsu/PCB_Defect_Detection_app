from fastapi import APIRouter
from .routers import pcb_defect_router, log_router

router = APIRouter()

router.include_router(pcb_defect_router.router)
router.include_router(log_router.router)