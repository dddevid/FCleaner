import os
import tempfile
import shutil
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def delete_temp_files():
    temp_dir = Path(tempfile.gettempdir())
    chrome_cache_dir = Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Cache"
    edge_cache_dir = Path("/data/data/com.microsoft.emmx/cache/Cache")
    firefox_cache_base_dir = Path.home() / "AppData/Local/Mozilla/Firefox/Profiles"
    brave_cache_dir = Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache"
    opera_gx_cache_dir = Path.home() / "AppData/Local/Opera Software/Opera GX Stable/Cache"

    deleted_files = 0
    skipped_files = 0

    # Funzione per eliminare file e cartelle in una directory specificata
    def delete_in_directory(directory):
        nonlocal deleted_files, skipped_files
        if directory.exists():
            for root, dirs, files in os.walk(directory):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        os.remove(file_path)
                        deleted_files += 1
                    except PermissionError:
                        skipped_files += 1
                    except Exception:
                        skipped_files += 1

                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(dir_path)
                        deleted_files += 1
                    except PermissionError:
                        skipped_files += 1
                    except Exception:
                        skipped_files += 1

    # Elimina i file temporanei
    delete_in_directory(temp_dir)

    # Elimina la cache di Chrome
    delete_in_directory(chrome_cache_dir)

    # Elimina la cache di Microsoft Edge
    delete_in_directory(edge_cache_dir)

    # Elimina la cache di Firefox
    if firefox_cache_base_dir.exists():
        for profile_dir in firefox_cache_base_dir.iterdir():
            firefox_cache_dir = profile_dir / "cache2"
            delete_in_directory(firefox_cache_dir)

    # Elimina la cache di Brave
    delete_in_directory(brave_cache_dir)

    # Elimina la cache di Opera GX
    delete_in_directory(opera_gx_cache_dir)

    messagebox.showinfo("Risultato", f"File eliminati: {deleted_files}\nFile saltati: {skipped_files}")

def on_closing():
    if messagebox.askokcancel("Esci", "Vuoi chiudere il programma?"):
        root.destroy()

root = tk.Tk()
root.title("Eliminatore di file temporanei e Cache Browser")

root.geometry("350x200")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Premi il pulsante per eliminare i file temporanei e la Cache dei Browser.")
label.pack(pady=10)

button = tk.Button(frame, text="Elimina file temporanei e Cache", command=delete_temp_files)
button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
