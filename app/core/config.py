import os

from dotenv import load_dotenv
from databases import DatabaseURL


load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "markqiu")
    MONGO_DB = os.getenv("MONGO_DB", "fastapi")

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

database_name = MONGO_DB
article_collection_name = "articles"
favorites_collection_name = "favorites"
tags_collection_name = "tags"
users_collection_name = "users"
comments_collection_name = "commentaries"
followers_collection_name = "followers"