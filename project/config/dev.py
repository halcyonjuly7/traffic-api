import os

API_KEY = "AIzaSyALBdrH4QFwe5ZE9_Y3G_M0RaSC56DBA2w"
DB_PASSWD = "Jiujitsu123"
DB_USERNAME = "postgres"
DB_HOSTADDR = "45.55.198.11"
PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
PICTURES_URL = "https://maps.googleapis.com/maps/api/place/photo"
STDOUT_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs", "api_out.logs")
STDERR_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs", "api_error.logs")