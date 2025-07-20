# 📁 Google Drive CLI Tool

A command-line interface (CLI) in Python for interacting with Google Drive.  
Supports uploading, downloading, deleting, and reading text from files in a specified Drive folder.

---

## ✨ Features

- 🔼 Upload a file to a Google Drive folder  
- 🔽 Download a file by name from the folder  
- 🗑️ Delete a file from the folder  
- 📖 Read and return text from `.txt`, `.md`, `.pdf`, and `.docx` files  
- ✅ OAuth-based authentication with token reuse  
- 🛠️ Organized, modular design (`main.py` + `drive_utils.py`)  
- 🔐 Uses `.env` for secure credential management  

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/theBEST-git/google_drive_cli.git
cd google_drive_cli
````

### 2. Install Dependencies (with `uv`)

```bash
uv pip install -r requirements.txt
```

### 3. Create and Configure Environment File

Copy the template:

```bash
cp .env.example .env
```

Then fill in your `.env` file with:

```env
GOOGLE_OAUTH_CLIENT=client_secret.json
```

Where `client_secret.json` is your OAuth 2.0 client file downloaded from Google Cloud Console.

### 4. Run the CLI Tool

```bash
python main.py
```

You'll be prompted to:

* Select an action: upload / download / delete
* Provide a file name
* Authenticate on the first run via a browser pop-up

---

## 📁 Folder Setup

All files are uploaded to this specific Drive folder:

```
FOLDER_ID = "1o3RwSMG9UYGWs9BgL9Xcoo97WqRuwqwE"
```

To use a different folder:

* Share your target Drive folder with your OAuth service account (if using service creds)
* Update `FOLDER_ID` in `main.py`

---

## 📄 Supported File Types for Text Extraction

```txt
✅ .txt  
✅ .md  
✅ .pdf  
✅ .docx
```

Other types will be skipped or partially read depending on format compatibility.

---

## 🧪 Project Structure

```
google_drive_cli/
│
├── main.py                # CLI entry point
├── drive_utils.py         # All Drive-related utility functions
├── .env.example           # Sample environment configuration
├── token.pkl              # Auto-generated OAuth token file
├── client_secret.json     # (You provide this)
└── requirements.txt       # Python dependencies
```

---

## 🔒 Environment Configuration (`.env`)

```env
GOOGLE_OAUTH_CLIENT=client_secret.json
```

*Make sure to keep your real `.env` and `client_secret.json` out of version control.*

---

## 📜 License

MIT License © 2025 [@theBEST](https://github.com/theBEST-git)

---

## 🙌 Acknowledgements

Built with:

* [Google Drive API](https://developers.google.com/drive)
* [google-api-python-client](https://github.com/googleapis/google-api-python-client)
* [google-auth](https://github.com/googleapis/google-auth-library-python)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 💡 Ideas for Future Improvements

* ✅ Progress bars for large file uploads/downloads
* 📂 Support for recursive folder uploads
* 🧠 AI-powered Drive search & summaries
* 🕒 Log and version history viewer

---

Happy automating! 🛠️📁
