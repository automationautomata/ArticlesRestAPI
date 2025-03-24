import os


DATABASE_URL = os.getenv("DATABASE_URL")

HOST = os.getenv("HOST")

PORT = os.getenv("PORT")

ADDRESS = f"{HOST}:{PORT}/"
