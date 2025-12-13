from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
import json

router = APIRouter(prefix="/tab", tags=["LOGS"])
templates = Jinja2Templates(directory="templates")

log_file = Path("static/logs/detections_log.json")

@router.get("/logs", response_class=HTMLResponse)
async def show_logs(request: Request):
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
        print("Смотри и изучай")
    else:
        print("Ошибка чтения логов! Нет лог-файла!")
        logs = []

    return templates.TemplateResponse("pcb_defect_logs.html", {
        "request": request,
        "logs": logs,
        "title": "Журнал детекций"
    })


@router.get("/logs/download/detections_log.json", response_class=FileResponse)
async def logs_json():
    return FileResponse(log_file, media_type='application/octet-stream', filename='{}.json'.format(log_file.stem))