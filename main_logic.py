import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from azure.storage.blob import BlobServiceClient

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


# ------ LISTAR DRIVE ------
def listar_drive_files():
    service = google_drive_auth()
    response = service.files().list(
        q=f"'{GOOGLE_FOLDER_ID}' in parents",
        fields="files(id, name)"
    ).execute()

    return response.get("files", [])


# ------ AZURE AUTH ------
def azure_auth():
    return BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)


# ------ LISTAR BLOB ------
def listar_destino_blob():
    blob = azure_auth()
    container = blob.get_container_client(AZURE_CONTAINER)
    return [b.name for b in container.list_blobs()]


# ------ MIGRAR ARQUIVOS ------
def migrar_arquivos():
    logs = []
    drive = google_drive_auth()
    azure = azure_auth()
    arquivos = listar_drive_files()

    for file in arquivos:
        nome = file["name"]
        logs.append(f"Baixando: {nome}")

        # Download
        request = drive.files().get_media(fileId=file["id"])
        data = request.execute()
        with open(nome, "wb") as f:
            f.write(data)

        logs.append(f"Enviando {nome}...")

        # Upload
        container = azure.get_container_client(AZURE_CONTAINER)
        with open(nome, "rb") as f:
            container.upload_blob(nome, f, overwrite=True)

        os.remove(nome)
        logs.append(f"✔ Concluído: {nome}")

    return logs
