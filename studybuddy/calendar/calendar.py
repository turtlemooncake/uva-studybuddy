import datetime
from datetime import timedelta
import pytz
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("credentials.json")
scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/calendar"])
CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

request_body = {
    "summary": "Study Buddy Meetups"
}