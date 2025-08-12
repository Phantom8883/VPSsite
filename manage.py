#!/usr/bin/env python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из корня проекта
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедись, что оно установлено и доступно в виртуальном окружении."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
