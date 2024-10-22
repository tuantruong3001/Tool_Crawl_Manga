import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
#from time import sleep


def download_img(img_url, chapter_folder, headers, progress_callback, total_images):
    img_name = os.path.basename(img_url.split("?")[0])  
    img_path = os.path.join(chapter_folder, img_name)  
    #for i in range(3): use this command if network is slow
    try:
        img_response = requests.get(img_url, headers=headers, timeout=5, verify=False)
        img_response.raise_for_status()
        
        with open(img_path, "wb") as img_file:
            img_file.write(img_response.content)

        print(f"Downloaded: {img_name} to folder {chapter_folder}")
    except Exception as e:
        print(f"Download error {img_url}: {e}")
        #sleep(0.5)
    finally:
        progress_callback()

def download_images(img_urls, chapter_folder, headers, progress_callback=None):
    total_images = len(img_urls)
    completed_images = 0

    def update_progress():
        nonlocal completed_images
        completed_images += 1
        if progress_callback:
            progress_callback(completed_images, total_images)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(download_img, img_url, chapter_folder, headers, update_progress, total_images) for img_url in img_urls]

    for future in as_completed(futures):
        future.result()