# 红楼梦人物剧照自动爬取&人脸识别并裁剪（自动标注）

**重要:** 如果这个项目有任何问题，请联系我：yuanchen1099@gmail.com  
**数据集:** images - 134张87版红楼梦人物角色剧照

## 背景
本项目是用于知识图谱语料库的数据集制作，主要需求是找出红楼梦人物角色剧照（主要集中在87版红楼梦，少量新版红楼梦），随后对其进行裁剪（人脸）。

## 说明

### 脚本:
- **catchImage.py**: 下载某个网页特定URL照片。
- **checkImage.py**: 已裁剪照片在Excel中标记（characters_faces中存在的图片，在names.xlsx中标记为“已处理”）。
- **ImagePostProcessing.py**: 本地图片人脸识别并标注算法。提取names.xlsx中标注不为“已处理”的人物，去images中找到并进行识别，识别后裁剪并存入characters_faces（覆盖存储）。
- **picturesAuto.py**: 自动去百度爬取照片并裁剪。

### 使用模型:
- **MTCNN** (多任务级联卷积网络)

### 需要的包:
> ```
> pip install pandas requests beautifulsoup4 pillow opencv-python
> ```

### 使用方法:
1. **下载特定图片:** 使用 `catchImage.py` 从指定的URL下载图片。
2. **标记已处理图片:** 使用 `checkImage.py` 更新 `names.xlsx`，将 `characters_faces` 中的图片标记为“已处理”。
3. **人脸识别和裁剪:** 使用 `ImagePostProcessing.py` 识别并裁剪本地图像中的人脸。提取 `names.xlsx` 中未标记为“已处理”的人物，在 `images` 文件夹中找到对应的图片，裁剪人脸，并保存到 `characters_faces` 文件夹。
4. **自动爬取和裁剪图片:** 使用 `picturesAuto.py` 自动从百度爬取图片并裁剪。

本项目旨在简化从《红楼梦》中收集和处理人物剧照的过程，从而更容易创建一个综合的数据集用于进一步分析和使用。
