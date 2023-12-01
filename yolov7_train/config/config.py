import os

from dotenv import load_dotenv

load_dotenv()
config = {
    "SQLALCHEMY_DATABASE_URI": os.environ.get("DATABASE_URL"),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "DB_USER_NAME": os.environ.get("user_name"),
    "DB_PASSWORD": os.environ.get("password"),
    "DB_HOST": os.environ.get("host"),
    "DB_NAME": os.environ.get("database_name"),
}
