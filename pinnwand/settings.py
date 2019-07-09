import os

DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///:memory:"
LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
