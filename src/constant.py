import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.pomidor-stage.ru"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded", "accept": "application/json"}
passData = {
    "username": f'{os.getenv("USER_LOGIN")}',
    "password": f'{os.getenv("USER_PASS")}'
}