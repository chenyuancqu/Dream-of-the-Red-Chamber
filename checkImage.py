"""
@Project : pythonProject1
@File    : checkImage.py
@Author  : chenyuan
@Email   : yuan_chen24@163.com
@Date    : 2024/6/12-15:30
@Description: 已裁剪照片在excel中标记（characters_faces中存在的图片，在names.xlsx中标记为“已处理”）
"""


import os
import pandas as pd

# 读取Excel表格中的人物名称
excel_path = 'names.xlsx'
df = pd.read_excel(excel_path)

# 获取人物名称列表（假设第一列是人物名称）
characters = df.iloc[:, 0].dropna().tolist()

# 设置文件夹路径
characters_faces_folder = 'characters_faces'

# 检查每个人物是否有对应的图像文件
for index, character in enumerate(characters):
    img_path = os.path.join(characters_faces_folder, f'{character}.jpg')
    if os.path.exists(img_path):
        df.at[index, '状态'] = '已处理'

# 将更新后的DataFrame保存回Excel文件
df.to_excel(excel_path, index=False)

print("检查完毕！")