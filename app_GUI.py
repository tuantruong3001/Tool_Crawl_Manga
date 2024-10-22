import tkinter
import customtkinter
from utils import is_valid_https_url, update_progress
import threading
import tkinter.messagebox as messagebox
from Site_Download.TruyenQQ import download_truyenqq, stopDownload
from Site_Download.Nettruyen import download_nettruyen

# Event to stop the download thread
stop_event = threading.Event()

def startDownload():
    base_url = link.get()
    selected_site = site_var.get()
    print(f"Start download from: {base_url} on site: {selected_site}")
    if not base_url:
        messagebox.showinfo("Information", "No URL provided")
        return
    if not is_valid_https_url(base_url):
        messagebox.showinfo("Information", "Invalid URL")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': f'{base_url}' 
    }

    def progress_callback(current, total):
        update_progress(current, total, pPercentage, progressBar)

    site_actions = {
    "TruyenQQ": lambda: download_truyenqq(base_url, headers, progress_callback),
    "Nettruyen": lambda: download_nettruyen(base_url, headers, progress_callback),
    "Cuutruyen": lambda: messagebox.showinfo("Information", "Site not supported yet"),
    "MangaDex": lambda: messagebox.showinfo("Information", "Site not supported yet")
    }

    if selected_site in site_actions:
        site_actions[selected_site]()
    else:
        messagebox.showinfo("Information", "Invalid site selected")

# Start download thread
def startDownloadThread():
    stop_event.clear()
    download_thread = threading.Thread(target=startDownload)
    download_thread.start()

# Clear fields    
def clearFields():
    url_var.set("")
    pPercentage.configure(text="0%")
    progressBar.set(0)

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("800x520")
app.title("Manga Download")

# UI elements
title = customtkinter.CTkLabel(app, text="Insert Link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=450, height=40, textvariable=url_var)
link.pack()

# Site selection dropdown
site_var = tkinter.StringVar(value="TruyenQQ")
site_dropdown = customtkinter.CTkOptionMenu(app, variable=site_var, values=["Nettruyen", "TruyenQQ"])
site_dropdown.pack(padx=20, pady=20)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownloadThread)
download.pack(padx=20, pady=20)

# Stop button
stop_button = customtkinter.CTkButton(app, text="Stop", command=stopDownload)
stop_button.pack(padx=20, pady=20)

# Clear button
clear_button = customtkinter.CTkButton(app, text="Clear", command=clearFields)
clear_button.pack(padx=20, pady=20)

# Progress bar
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

if __name__ == "__main__":
    app.mainloop()