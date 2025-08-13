import os
import json
from firebase_admin import credentials, initialize_app

firebase_config = os.getenv("FIREBASE_CREDENTIALS")

if firebase_config:
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)
    initialize_app(cred)
else:
    raise FileNotFoundError("No Firebase credentials found in environment variables")
