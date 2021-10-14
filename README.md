# 0xTracker Backend API

.env file should contain the following


MONGODB_URL = "mongodb+srv://"

MONGO_DB="myFirstDatabase"

COVALENT_API = 'ckey_xxxxxxxxxxxxxxxxxxxxxx'

To start the api run the following from root:

uvicorn main:app --app-dir app --reload
