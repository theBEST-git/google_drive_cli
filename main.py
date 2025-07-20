from drive_utils import (
    check_if_file_exists,
    upload_file_to_drive,
    download_file_from_drive,
    delete_file_from_drive,
    read_file_text_from_drive
)

FOLDER_ID = "1o3RwSMG9UYGWs9BgL9Xcoo97WqRuwqwE"

def main():
    while True:
        status = input(
            "Would you like to upload, download, or delete a file?\n"
            "Enter 'ul' to upload, 'dl' to download, 'del' to delete, 'read' to read text, or 'exit' to quit: "
        ).strip().lower()

        if status in ["ul", "dl", "del", "read"]:
            break
        elif status == "exit":
            print("👋 Exiting the program.")
            return
        else:
            print("❌ Invalid option. Please enter 'ul', 'dl', 'del', or 'exit'.")

    # Ask for the filename
    file_name = input("Please enter the filename (e.g., myfile.txt): ").strip()

    if status == "ul":
        existing = check_if_file_exists(file_name, folder_id=FOLDER_ID)
        if existing:
            print("⚠️ File already exists – no need to re-upload or please rename the file.")
        else:
            upload_file_to_drive(file_name, parent_folder_id=FOLDER_ID)
            print("✅ Upload complete.")

    elif status == "dl":
        existing = check_if_file_exists(file_name, folder_id=FOLDER_ID)
        if existing:
            download_file_from_drive(filename=file_name, folder_id=FOLDER_ID)
        else:
            print("❌ File not found in Google Drive folder.")

    elif status == "del":
        existing = check_if_file_exists(file_name, folder_id=FOLDER_ID)
        if existing:
            confirm = input(f"Are you sure you want to delete '{file_name}'? (y/n): ").strip().lower()
            if confirm == "y":
                delete_file_from_drive(filename=file_name, folder_id=FOLDER_ID)
        else:
            print("❌ File not found in Google Drive folder.")

    elif status == "read":
        content = read_file_text_from_drive(file_name, folder_id=FOLDER_ID)
        if content:
            print("📝 File content preview:")
            print(content[:2000])  # Preview first 2000 characters
        else:
            print("⚠️ Unable to extract content.")


if __name__ == "__main__":
    main()
