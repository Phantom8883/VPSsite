# core/settings/load_env.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Путь до файла .env — считаем, что он лежит в корне проекта рядом с manage.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Загружаем .env
load_dotenv(dotenv_path=BASE_DIR / '.env')
