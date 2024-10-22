import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from downloader import download_images
from utils import create_download_directory
import threading
import tkinter.messagebox as messagebox


def stopDownload():
    stop_event.set()
    
# Event to stop the download thread
stop_event = threading.Event()

def download_truyenqq(base_url, headers, progress_callback):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    chapter_container_class = "works-chapter-list"
    chapter_container = soup.find("div", class_=chapter_container_class)

    # Create folder to store images
    folder_name = soup.title.string
    folder_name = re.sub(r'[<>:"/\\|?*]', '', folder_name)
    download_path = create_download_directory("Downloads")
    folder_download = os.path.join(download_path, folder_name)

    chapter_links = chapter_container.find_all("a", href=True) if chapter_container else []

    try:
        for chapter_link in chapter_links:
            if stop_event.is_set():
                messagebox.showinfo("Information", "Download Stopped")
                return

            chapter_name = chapter_link.text.strip()  
            if "Chương" in chapter_name:  
                chapter_name = chapter_name.replace(" ", "_")  
                chapter_name = ''.join(e for e in chapter_name if e.isalnum() or e in "_-")  
                chapter_folder = os.path.join(folder_download, chapter_name)  

                os.makedirs(chapter_folder, exist_ok=True)

                chapter_url = urljoin(base_url, chapter_link['href'])  
                print(f"Download from: {chapter_url}")

                chapter_response = requests.get(chapter_url)
                chapter_soup = BeautifulSoup(chapter_response.text, "html.parser")
                img_tags = chapter_soup.find_all("img", class_="lazy") 

                if not img_tags:
                    print(f"Can't find image from {chapter_url}")
                    continue

                img_urls = [urljoin(chapter_url, img_tag.get("src")) for img_tag in img_tags]

                download_images(img_urls, chapter_folder, headers, progress_callback)
    except Exception as e:
        print("Error: " + str(e))

    messagebox.showinfo("Information", "Download Completed to " + os.path.join(download_path, folder_download))
    