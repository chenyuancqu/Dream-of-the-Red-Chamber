"""
@Project : pythonProject1
@File    : catchImage.py
@Author  : chenyuan
@Email   : yuan_chen24@163.com
@Date    : 2024/6/11-16:56
@Description: 下载某个网页特定url照片
"""

import os
import requests
from PIL import Image
from io import BytesIO

# 创建文件夹
def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# 下载并保存图片
def download_image(url, folder_name, img_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'http://www.360doc.com/'  # 加入Referer头
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        # 转换为RGB模式（以处理所有图像类型）
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img_path = os.path.join(folder_name, f"{img_name}.jpg")
        img.save(img_path, 'JPEG')
        print(f"Downloaded and converted image {img_name} from {url}")
    except Exception as e:
        print(f"Could not download or convert image {img_name} from {url}: {e}")

# 主流程
def main():
    base_url = "http://image.360doc.com/DownloadImg/9737/352029_"
    start_index = 2
    end_index = 97
    folder_name = 'downloaded_images'

    # 创建文件夹
    create_directory(folder_name)

    # 下载并保存图片
    for i in range(start_index, end_index + 1):
        img_url = f"{base_url}{i}"
        download_image(img_url, folder_name, f"{i}")

    print("Process completed.")

if __name__ == "__main__":
    main()
