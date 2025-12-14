from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import HTMLResponse,StreamingResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
import json

from src.services.logger import iterfile, remove_file, build_zip

router = APIRouter(prefix="/tab", tags=["LOGS"])
templates = Jinja2Templates(directory="templates")

zip_name = "full_detections.zip"
zip_path = Path("static/logs") / zip_name
uploads_dir = Path("static/uploads")

log_filename = "detections_logs.json"
log_path = Path("static/logs") / log_filename

@router.get("/logs", response_class=HTMLResponse)
async def show_logs(request: Request):
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        print("Ошибка чтения логов! Нет лог-файла!")
        logs = []

    return templates.TemplateResponse("pcb_defect_logs.html", {
        "request": request,
        "logs": logs,
        "title": "Журнал детекций"
    })

@router.get("/logs/download/json", response_class=StreamingResponse)
async def download_logs_json():
    return StreamingResponse(iterfile(log_path), media_type="application/json", headers={"Content-Disposition": f"attachment; filename={log_filename}"})


@router.get("/logs/download/zip", response_class=StreamingResponse)
async def download_full_zip(background_tasks: BackgroundTasks):
    build_zip(
        zip_path=zip_path,
        images_dir=uploads_dir,
        log_path=log_path
    )
    background_tasks.add_task(remove_file, zip_path)
    return StreamingResponse(iterfile(zip_path), media_type="application/zip",
                             headers={"Content-Disposition": f"attachment; filename={zip_name}"})