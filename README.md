[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1%2B-red)]()
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119%2B-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

# PCB Defect Detection — YOLOv8 + FastAPI

<div align="center">
  <img width="800" alt="pcb-detection-demo" src="static/assets/icons/pred_example.jpg" />
</div>

---

## Краткое описание

**PCB Defect Detection** — это веб-приложение для **автоматического обнаружения и анализа дефектов печатных плат**  
на основе **YOLOv8 (Ultralytics)** и **FastAPI**.

Приложение принимает одно или несколько изображений печатных плат, выполняет детектирование дефектов,
визуализирует bounding box’ы, рассчитывает **процент повреждения платы по площади**  
и формирует **журнал детекций** с возможностью выгрузки результатов.

---

## Обнаруживаемые дефекты

Модель обучена распознавать следующие типы дефектов:

- `missing_hole` — отсутствующее отверстие  
- `mouse_bite` — повреждение дорожки в цепи  
- `open_circuit` — обрыв цепи  
- `short` — короткое замыкание  
- `spur` — выступ  
- `spurious_copper` — лишняя медь  

---

## Основные возможности

- Применение **YOLOv8m** в проекте
- **Загрузка нескольких изображений**
- Настраиваемый **порог уверенности**
- Фильтрация по классам дефектов
- **Расчёт процента повреждения платы** по площади дефектов
- Автоматическое логирование результатов в JSON-формат
- Выгрузка **ZIP-архива** с изображениями, которые уже прошли обработку  + логи детекции
- Удобный и продуманный web-интерфейс
- Асинхронный FastAPI backend

---

## Установка
> Для работы приложения требуется Python 3.11.9
- Клонируйте репозиторий в вашу среду разработки:
	```
	git clone https://github.com/Arthicsu/PCB_Defect_Detection_app.git
	```
- Установите все необходимые модули и библиотеки:
	```
	pip install -r requirements.txt
	```
- Запустите приложение:
	```
	uvicorn src.main:app --reload
	```

## Использование
1. Перейдите по адресу `http://localhost:8000`.
2. Выберите изображение и нажмите "Запустить детектирование".

## Лицензия
- Этот проект распространяется под лицензией MIT.