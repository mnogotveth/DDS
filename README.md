# DDS — Django/DRF

## Установка
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt

## Миграции и стартовые данные
python manage.py makemigrations
python manage.py migrate
## Запуск сидера
python manage.py loaddata fixtures/seed.json

## создание админа
python manage.py createsuperuser

## запуск
cd dds_project
python manage.py runserver

![Скриншот 1](docs/images/2025-09-02_16-38-50.png)
![Скриншот 2](docs/images/2025-09-02_16-38-59.png)
![Скриншот 3](docs/images/2025-09-02_16-39-08.png)
![Скриншот 4](docs/images/2025-09-02_16-39-31.png)
![Скриншот 5](docs/images/2025-09-02_16-39-38.png)
![Скриншот 6](docs/images/2025-09-02_16-39-54.png)
![Скриншот 7](docs/images/2025-09-02_16-40-14.png)
![Скриншот 8](docs/images/2025-09-02_16-40-22.png)
![Скриншот 9](docs/images/2025-09-02_16-40-33.png)
![Скриншот 10](docs/images/2025-09-02_16-40-44.png)
