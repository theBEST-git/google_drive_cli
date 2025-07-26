from rich import print
from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.panel import Panel

from basic_drive_utils import (
    check_if_file_exists,
    upload_file_to_drive,
    download_file_from_drive,
    delete_file_from_drive,
    read_file_text_from_drive
)

FOLDER_ID = "1o3RwSMG9UYGWs9BgL9Xcoo97WqRuwqwE"
console = Console()

def main():
    console.print(
        Panel.fit(
            "📂 [bold cyan]                       Google Drive File Manager                       [/bold cyan]",
            subtitle="ul = Upload | dl = Download | del = Delete | read = Read | exit = Quit",
            subtitle_align="left",
            style="green",
            width=300
        )
    )

    while True:
        status = Prompt.ask(
            "[bold yellow]Choose an action[/bold yellow] [ul/dl/del/read/exit]",
            choices=["ul", "dl", "del", "read", "exit"],
            default="ul"
        )

        if status == "exit":
            print("[bold green]👋 Exiting the program.[/bold green]")
            return
        else:
            break

    file_name = Prompt.ask("[bold blue]Enter the filename[/bold blue] (e.g., myfile.txt)")

    if status == "ul":
        if check_if_file_exists(file_name, folder_id=FOLDER_ID):
            console.print("⚠️ [yellow]File already exists – no need to re-upload or please rename the file.[/yellow]")
        else:
            upload_file_to_drive(file_name, parent_folder_id=FOLDER_ID)
            console.print("✅ [green]Upload complete.[/green]")

    elif status == "dl":
        if check_if_file_exists(file_name, folder_id=FOLDER_ID):
            download_file_from_drive(filename=file_name, folder_id=FOLDER_ID)
            console.print("✅ [green]Download complete.[/green]")
        else:
            console.print("❌ [red]File not found in Google Drive folder.[/red]")

    elif status == "del":
        if check_if_file_exists(file_name, folder_id=FOLDER_ID):
            confirm = Confirm.ask(f"[red]Are you sure you want to delete '{file_name}'?[/red]")
            if confirm:
                delete_file_from_drive(filename=file_name, folder_id=FOLDER_ID)
                console.print(f"🗑️ [bold red]'{file_name}' deleted successfully.[/bold red]")
        else:
            console.print("❌ [red]File not found in Google Drive folder.[/red]")

    elif status == "read":
        content = read_file_text_from_drive(file_name, folder_id=FOLDER_ID)
        if content:
            console.rule("📝 File Content Preview")
            print(f"[dim]{content[:2000]}[/dim]")  # Preview only first 2000 characters
        else:
            console.print("⚠️ [yellow]Unable to extract content.[/yellow]")

if __name__ == "__main__":
    main()
