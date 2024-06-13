"""
@Project : pythonProject1
@File    : ImagePostProcessing.py
@Author  : chenyuan
@Email   : yuan_chen24@163.com
@Date    : 2024/6/12-09:26
@Description: 本地图片人脸识别并标注算法
提取names.xlsx中标注不为“已处理”的人物，去images中找到并进行识别，识别后裁剪并存入characters_faces（覆盖存储）
"""



import os
import pandas as pd
from PIL import Image
import numpy as np
from mtcnn import MTCNN

# 读取Excel表格中的人物名称，并筛选出未处理的
excel_path = 'names.xlsx'
df = pd.read_excel(excel_path)

# 筛选出没有标记为“已处理”的人物
df_to_process = df[df.iloc[:, 1] != '已处理']

# 获取需要处理的人物名称列表（假设第一列是人物名称）
characters_to_process = df_to_process.iloc[:, 0].dropna().tolist()

# 设置文件夹路径
images_folder = 'images'
output_folder = 'characters_faces'

# 创建存储图片的文件夹（如果不存在则创建）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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

# 处理函数，获取图片并进行裁剪
def process_character(character, index):
    img_path = os.path.join(images_folder, f'{character}.jpg')
    if not os.path.exists(img_path):
        print(f"未找到图片：{img_path}")
        return

    try:
        img = Image.open(img_path)
        face_img = crop_face(img)
        if face_img:
            face_img.save(os.path.join(output_folder, f'{character}.jpg'))
            print(f"{character} 的图片已保存")
            df.at[index, df.columns[1]] = '已处理'
        else:
            print(f"未检测到 {character} 的人脸")
    except Exception as e:
        print(f"处理 {character} 的图片时出错：{e}")

# 搜索并处理每个人物的图片
for index, row in df_to_process.iterrows():
    name = row.iloc[0]
    print(f"正在处理: {name}")
    process_character(name, index)

# 将更新后的DataFrame保存回Excel文件
df.to_excel(excel_path, index=False)

print("处理完毕！")