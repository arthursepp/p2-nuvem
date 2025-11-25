import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from azure.storage.blob import BlobServiceClient

# Carregar variáveis de ambiente
load_dotenv()

GOOGLE_FOLDER_ID = os.getenv("GOOGLE_FOLDER_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")

# ------ GOOGLE AUTH ------
def google_drive_auth():
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

# ...existing code...