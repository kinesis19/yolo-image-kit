# yolo-image-kit 🛠️
Stop manually preparing images for YOLO. A simple desktop app to automate your dataset workflow.
`yolo-image-kit` is a straightforward desktop application designed to streamline the tedious process of preparing image datasets for YOLO object detection training.

---

## 📸 Screenshots
| Image Resizing Tab | Extract frames from Video |
| :----------------- | :------------------------ |
| ![img_image_resizing_tab](/assets/img_image_resizing_tab.png) | ![img_video_to_frames_tab](/assets/img_video_to_frames_tab.png) |




## ✨ Key Features
- Batch Image Resizing: Resize thousands of images to your desired resolution in a single run.
- Sequential Renaming: Automatically rename files with a custom prefix and sequential numbering (eg., `box_0001`, `box_0002`).
- Format Conversion: Convert various image formats(`PNG`, `BMP`, `HEIC`, etc.) to a standard format like `JPG`.
- Intuitive GUI: An easy-to-use graphical interface allows you to set up your processing task with just a few clicks.
- Cross-platform: Runs on both Windows and Linux (Ubuntu).


## ⚙️ Tech Stack
- **Python**: Main programming language
- **PySide6**: GUI Framework (Qt for Python)
- **OpenCV**: Processing video frames
- **Pillow**: Resizing and processing image


## 🚀 Installation & Usage

### 1. Clone Repository
```bash
git clone https://github.com/kinesis19/yolo-image-kit.git
cd yolo-image-kit
```

### 2. Setup Virtual Environment
```bash
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```python
pip install -r requirements.txt
```

### 4. Run the Application
```python
python3 main.py
```


## 📖 How to Use
### 🖼️ Image Resizing
1. Click the `Image Resizing` Tab.
2. Set the `Input Folder` to the directory containing your source images.
3. Set the `Output Folder` where the converted images will be saved.
4. Enter the desired `Image Size` (width x height) and `File Name Prefix`.
5. Click the `Start Conversion`.

### 🎞️ Video to Frames
1. Click the `Video to Frames` Tab.
2. Select your source video in the `Video File` field.
3. Set the `Output Folder` where the extracted frames will be saved.
4. Enter the desired `Frame Name Prefix`
5. Click the `Start Conversion`.

## 📜 License
This project is licensed under the MIT License.