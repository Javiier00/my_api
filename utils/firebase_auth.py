import os, json, base64
from firebase_admin import credentials, initialize_app


firebase_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")


firebase_json = json.loads(base64.b64decode(firebase_base64))


cred = credentials.Certificate(firebase_json)
initialize_app(cred)
