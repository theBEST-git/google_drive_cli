import os, pickle
from pathlib import Path
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
print("✅ All libs imported")

load_dotenv()
print("✅ All environment variables loaded")

SCOPES = ["https://www.googleapis.com/auth/drive.file"]  # only lets script manage files it created
CLIENT_FILE = os.getenv("GOOGLE_OAUTH_CLIENT")
TOKEN_FILE  = Path("token.pkl")
print(f"📁 OAuth client file: {CLIENT_FILE}")
print(f"🧪 Token file path: {TOKEN_FILE.resolve()}")

def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = pickle.loads(TOKEN_FILE.read_bytes())
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_bytes(pickle.dumps(creds))
    print("✅ Creds obtained")
    return creds

drive_service = build("drive", "v3", credentials=get_credentials())
print("✅ Google Drive service ready")

def upload_file_to_drive(filepath, filename=None, mimetype="application/octet-stream", parent_folder_id=None):
    if filename is None:
        filename = os.path.basename(filepath)

    file_metadata = {"name": filename}
    if parent_folder_id:
        file_metadata["parents"] = [parent_folder_id]

    media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)  # <-- resumable!
    
    print(f"🚀 Uploading '{filename}'...")
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name"
    ).execute()

    print(f"✅ Uploaded '{filename}' with ID: {uploaded_file['id']}")
    return uploaded_file


from googleapiclient.http import MediaIoBaseDownload
import io

def download_file_from_drive(filename, folder_id, save_as=None):
    """Downloads a file by name from a given Google Drive folder."""
    print(f"🔍 Searching for file: {filename} in folder ID: {folder_id}")

    # Search for the file inside the specified folder
    query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
    ).execute()

    files = results.get("files", [])
    if not files:
        print("❌ File not found.")
        return

    file = files[0]  # Download the first match
    file_id = file["id"]
    file_name = save_as or file["name"]

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    print(f"⬇️  Downloading '{file_name}'...")
    while not done:
        status, done = downloader.next_chunk()
        print(f"📦 Download progress: {int(status.progress() * 100)}%")

    print(f"✅ Download complete: {file_name}")

def check_if_file_exists(filename, folder_id):
    """Check if a file with the given name exists in a specific Drive folder."""
    query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name, modifiedTime, mimeType)",
    ).execute()

    files = results.get("files", [])
    if files:
        file = files[0]
        print(f"🔎 Found file: {file['name']} (ID: {file['id']}, modified: {file['modifiedTime']})")
        return file
    else:
        print("✅ The file is unique.")
        return None
    
def delete_file_from_drive(filename, folder_id):
    """Deletes the first file matching the filename in the specified folder."""
    print(f"🗑 Attempting to delete file: {filename} from folder ID: {folder_id}")

    query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
    ).execute()

    files = results.get("files", [])
    if not files:
        print("❌ No matching file found to delete.")
        return False

    file = files[0]
    file_id = file["id"]

    drive_service.files().delete(fileId=file_id).execute()
    print(f"✅ File '{filename}' (ID: {file_id}) deleted successfully.")
    return True

from PyPDF2 import PdfReader
from docx import Document

def read_file_text_from_drive(filename, folder_id):
    """Downloads a file from Drive and extracts text content as a string."""
    print(f"📥 Reading file content: {filename}")
    file = check_if_file_exists(filename, folder_id)
    if not file:
        print("❌ File not found in Drive.")
        return None

    # Temp local path to download
    temp_path = Path("_temp_" + filename)
    download_file_from_drive(filename, folder_id, save_as=temp_path)

    ext = temp_path.suffix.lower()
    content = ""

    try:
        if ext in [".txt", ".md", ".csv", ".py", ".json"]:
            content = temp_path.read_text(encoding="utf-8")

        elif ext == ".pdf":
            reader = PdfReader(str(temp_path))
            content = "\n".join(page.extract_text() or "" for page in reader.pages)

        elif ext == ".docx":
            doc = Document(str(temp_path))
            content = "\n".join(p.text for p in doc.paragraphs)

        else:
            print(f"⚠️ Unsupported file type: {ext}")
            return None

        print(f"✅ Extracted {len(content)} characters.")
        return content.strip()

    finally:
        if temp_path.exists():
            temp_path.unlink()  # clean up

print("--------------------ALL UTILS ARE READY--------------------")