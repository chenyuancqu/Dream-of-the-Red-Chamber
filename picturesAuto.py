"""
@Project : pythonProject1
@File    : picturesAuto.py
@Author  : chenyuan
@Email   : yuan_chen24@163.com
@Date    : 2024/6/12-09:35
@Description : 自动去百度爬去照片并裁剪
"""

import os
import time
import pandas as pd
import requests
from PIL import Image
import numpy as np
from bs4 import BeautifulSoup
from mtcnn import MTCNN
from io import BytesIO

# 读取Excel表格中的人物名称，并筛选出未处理的
excel_path = 'names.xlsx'
df = pd.read_excel(excel_path)

# 筛选出没有标记为“已处理”的人物
df_to_process = df[df.iloc[:, 1] != '已处理']

# 获取人物名称列表（假设第一列是人物名称）
characters = df_to_process.iloc[:, 0].dropna().tolist()

# 创建存储图片的文件夹
output_folder = 'characters_faces'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 使用百度图片搜索API发送请求，解析返回的JSON数据，提取图片URL
def search_baidu(character):
    search_queries = [f"红楼梦 {character} 图片",
                      f"红楼梦 {character}定妆照",
                      f"87版红楼梦 {character}剧照",
                      character]
    search_url = f"https://image.baidu.com/search/acjson"
    img_urls = []
    for search_query in search_queries:
        params = {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'queryWord': search_query,
            'word': search_query,
            'pn': '0',
            'rn': '120'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            results = response.json()
            img_urls.extend([result.get('thumbURL') for result in results.get('data', []) if result.get('thumbURL')])
        except requests.exceptions.RequestException as e:
            print(f"搜索 {character} 的图片时出错：{e}")

    return img_urls

# 使用百度百科词条页面获取图片URL
def search_baidu_baike(character):
    search_url = f"https://baike.baidu.com/item/{character}"
    img_urls = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls.extend([img['src'] for img in img_tags if 'src' in img.attrs and img['src'].startswith('http')])
    except requests.exceptions.RequestException as e:
        print(f"搜索 {character} 的图片时出错：{e}")

    print(f"{character} 的图片URL: {img_urls}")  # 输出调试信息
    return img_urls

# 使用必应图片搜索API发送请求，解析返回的JSON数据，提取图片URL
def search_bing(character):
    search_url = f"https://api.bing.microsoft.com/v7.0/images/search"
    img_urls = []
    for search_query in [f"红楼梦 {character} 图片",
                         f"红楼梦 {character}定妆照",
                         f"87版红楼梦 {character}剧照",
                         character]:
        params = {
            'q': search_query,
            'license': 'public',
            'imageType': 'photo'
        }
        headers = {
            'Ocp-Apim-Subscription-Key': 'YOUR_API_KEY_HERE'  # 将 YOUR_API_KEY_HERE 替换为你的API密钥
        }
        try:
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            results = response.json()
            img_urls.extend([image['thumbnailUrl'] for image in results.get('value', []) if 'thumbnailUrl' in image])
        except requests.exceptions.RequestException as e:
            print(f"搜索 {character} 的图片时出错：{e}")

    return img_urls

# 使用搜狗图片搜索API发送请求，解析返回的JSON数据，提取图片URL
def search_image_sogou(character):
    search_queries = [f"红楼梦 {character} 图片",
                      f"红楼梦 {character}定妆照",
                      f"87版红楼梦 {character}剧照",
                      character]
    search_url = f"https://pic.sogou.com/pics"
    img_urls = []
    for search_query in search_queries:
        params = {
            'query': search_query,
            'mode': '1',
            'start': '0',
            'reqType': 'ajax',
            'reqFrom': 'result',
            'tn': '0'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://pic.sogou.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
        try:
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            results = response.json()
            img_urls.extend([result.get('thumbUrl') for result in results.get('items', []) if result.get('thumbUrl')])
        except requests.exceptions.RequestException as e:
            print(f"搜索 {character} 的图片时出错：{e}")

    return img_urls


# 发送HTTP请求下载图片，将响应内容转换为PIL图像对象
def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except requests.exceptions.RequestException as e:
        print(f"下载图片 {url} 时出错：{e}")
        return None


# 使用 MTCNN 模型检测人脸，如果检测到人脸则裁剪并返回
def crop_face(image):
    detector = MTCNN()
    img_np = np.array(image.convert("RGB"))  # 将图像转换为RGB格式
    faces = detector.detect_faces(img_np)
    if len(faces) == 0:
        return None  # 没有检测到人脸
    for face in faces:
        x, y, w, h = face['box']
        face_img = img_np[y:y + h, x:x + w]
        face_pil = Image.fromarray(face_img)
        return face_pil


# 处理函数，获取搜索图片的前五个URL并进行裁剪
def process_character(character):
    # img_urls = search_baidu_baike(character)
    img_urls = search_baidu(character)
    if not img_urls:
        print(f"未搜索到有效的图片URL：{character}")
        return False

    for url in img_urls[:5]:  # 尝试前五个搜索结果
        img = download_image(url)
        if img:
            face_img = crop_face(img)
            if face_img:
                face_img.save(os.path.join(output_folder, f'{character}.jpg'))
                print(f"{character} 的图片已保存")
                return True
        time.sleep(1)  # 为了避免频繁请求被封禁，可以在每次请求后加一个短暂的延时
    return False

# 搜索并处理每个人物的图片
for i, character in enumerate(characters):
    print(f"正在处理: {character}")
    if process_character(character):
        if df.shape[1] > 1:
            df.loc[df.iloc[:, 0] == character, df.columns[1]] = "已处理"
    time.sleep(2)  # 每处理一个人物，延时以避免被封禁

# 保存处理状态到Excel
df.to_excel(excel_path, index=False)

print("处理完毕！")