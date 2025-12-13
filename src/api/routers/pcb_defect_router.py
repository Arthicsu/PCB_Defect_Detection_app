from fastapi import APIRouter, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.logger import append_to_json_file

from ultralytics import YOLO
import cv2

from pathlib import Path
from datetime import datetime
import numpy as np
import json, os


router = APIRouter()
templates = Jinja2Templates(directory="templates")

model_path = "src/models/detect/train6/weights/best.pt"
classes_path = "src/models/pcb_defect_classes.json"
uploads_folder = Path("static/uploads")


if os.path.exists(model_path) and os.path.exists(classes_path):
    try:
        model = YOLO(model_path)
        with open(classes_path, 'r', encoding='utf-8') as f:
            class_names = json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")
        class_names = {}
else:
    print("Модель не найдена")
    class_names = {}

@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("pcb_defect_form.html", {
        "request": request,
        "classes": class_names,
        "title": "Распознавание дефектов на печатных платах"
    })

@router.post("/predict", response_class=HTMLResponse)
async def predict_defect( #bro what. . .
        request: Request,
        file: UploadFile = File(...),
        threshold: float = Form(50.0),
        selected_classes: str = Form("")
    ):
    try:
        file_bytes = await file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        confidence_threshold = threshold / 100.0

        if selected_classes:
            selected_classes_list = [
                cls.strip().lower()
                for cls in selected_classes.split(",")
                if cls.strip()
            ]
        else:
            selected_classes_list = []

        results = model(img)[0]

        detections = []
        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            defect_area = (x2 - x1) * (y2 - y1)


            detections.append({
                "class_id": cls,
                "class_name": class_names[str(cls)],
                "confidence": round(conf, 3),
                "bbox": [x1, y1, x2, y2],
                "bbox_area": defect_area
            })


            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{class_names[str(cls)]} {conf:.2f}",(x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)

        img_path = uploads_folder / f"pred_{file.filename}"
        cv2.imwrite(str(img_path), img)

        log = {
            "filename": file.filename,
            "threshold": confidence_threshold,
            "selected_classes": selected_classes_list,
            "img_path": str(img_path),
            "detections": detections,
            "timestamp": datetime.utcnow().isoformat()
        }

        append_to_json_file("static/logs/detections_log.json", log)

        return templates.TemplateResponse("pcb_defect_result.html", {
            "request": request,
            "image_url": img_path,
            "threshold": confidence_threshold,
            "selected_classes": selected_classes_list,
            "detections": detections,
            "title": "Результат детектирования"
        })

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e), "status_code": 500})