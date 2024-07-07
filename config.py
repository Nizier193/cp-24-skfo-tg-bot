class Providers:
    RAGAPP = 'ragapp'
    RAGFLOW = 'ragflow'

class Config:
    FILEBASE = "data/"

    RAGFLOW_API = "ragflow-MzMjI0MzMwMzlmODExZWY5NDllMDI0Mm"
    RAGFLOW_URL = "http://127.0.0.1/v1/api/"

    RAGAPP_URL = "https://cp-24-skfo.open-core.ru/api/"

    TELEGRAM_API = "<Your telegram bot api_key>"
    DATABASE_DIR = "db_directory/db.db"

    PROVIDER = Providers.RAGAPP
