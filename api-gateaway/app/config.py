from dotenv import load_dotenv
import os
load_dotenv()

PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL")
AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")