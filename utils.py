import os
import re

def is_valid_https_url(url):
    pattern = r'^https:\/\/[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(:[0-9]{1,5})?(\/[^\s]*)?$'
    return re.match(pattern, url) is not None  
    
def create_download_directory(folder):
    download_path = os.path.join(os.getcwd(), folder)
    os.makedirs(download_path, exist_ok=True)
    return download_path

def update_progress(current, total, pPercentage, progressBar):
    percentage = (current / total) * 100
    pPercentage.configure(text=f"{percentage:.2f}%")
    progressBar.set(current / total)