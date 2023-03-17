from starlette.config import Config

config = Config(".env")
# DB
DB_HOST = config("DB_HOST", cast=str, default="127.0.0.1")
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_USER = config("DB_USER", cast=str, default="root")
DB_PASSWORD = config("DB_PASSWORD", cast=str, default="root")
DB_NAME = config("DB_NAME", cast=str, default="open_social")

# Uvicorn
HTTP_PORT = config("HTTP_PORT", cast=int, default=8080)
HTTP_HOST = config("HTTP_HOST", cast=str, default="0.0.0.0")


#ACCESS_TOKEN_EXPIRE_MINUTES = config("ITC_ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=120) # Session time in minutes
#ALGORITHM = "HS256"
#SECRET_KEY = config("ITC_SECRET_KEY", cast=str, default="212646234g2634234f23642fc46234c2634")
#USERS_STORAGE = config("ITC_USERS_STORAGE", cast=str)
#API_VER = config("ITC_API_VER", cast=str)
