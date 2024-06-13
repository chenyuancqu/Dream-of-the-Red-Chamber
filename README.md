# Extraction and Cropping of Characters from *Dream of the Red Chamber*

**Important:** If you encounter any issues with this project, please contact me at: yuanchen1099@gmail.com  
**Dataset:** images - 134 stills of characters from the 1987 version of *Dream of the Red Chamber*

## Background
This project is designed for creating a dataset for a knowledge graph corpus, focusing on extracting character stills from the TV series *Dream of the Red Chamber* (mainly the 1987 version, with some images from newer versions). The primary task involves finding and cropping these stills to focus on the characters' faces.

## Description

### Scripts:
- **catchImage.py**: Downloads images from specific URLs on a webpage.
- **checkImage.py**: Marks cropped images in an Excel file (images present in `characters_faces` are marked as "processed" in `names.xlsx`).
- **ImagePostProcessing.py**: Performs local face recognition and annotation. Extracts characters not marked as "processed" from `names.xlsx`, identifies faces in `images`, crops the faces, and saves them to `characters_faces` (overwriting existing images).
- **picturesAuto.py**: Automatically scrapes images from Baidu and crops them.

### Model Used:
- **MTCNN** (Multi-task Cascaded Convolutional Networks)

### Required Packages:
> ```
> pip install pandas requests beautifulsoup4 pillow opencv-python
> ```

### Usage:
1. **Download Specific Images:** Use `catchImage.py` to download images from a specified URL.
2. **Mark Processed Images:** Use `checkImage.py` to update `names.xlsx`, marking images in `characters_faces` as "processed".
3. **Face Recognition and Cropping:** Use `ImagePostProcessing.py` to recognize and crop faces in local images. It identifies characters not marked as "processed" in `names.xlsx`, finds corresponding images in `images`, crops the faces, and saves them to `characters_faces`.
4. **Automatic Image Scraping and Cropping:** Use `picturesAuto.py` to automatically scrape images from Baidu and crop them.

This project aims to streamline the process of gathering and processing character images from *Dream of the Red Chamber*, making it easier to create a comprehensive dataset for further analysis and use.
