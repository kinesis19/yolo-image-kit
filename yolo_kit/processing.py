import os
import cv2
from PIL import Image

def extract_frames_from_video(video_path, output_dir, naming_prefix):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            yield f"Create folder: '{output_dir}'"

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            yield f"Error: '{video_path}'"
            return
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        yield f"Start convert... (total frame: {total_frames})"

        count = 0;
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # Set file name
            new_filename = f"{naming_prefix}_{str(count + 1).zfill(4)}.jpg"
            output_path = os.path.join(output_dir, new_filename)

            # Save frame
            cv2.imwrite(output_path, frame)
            count += 1

            if count % 30 == 0:
                yield f"Converting: {count} / {total_frames}"
        
        cap.release()
        yield f"Convert done! Total {count} frame saved."

    except Exception as e:
        yield f"Critical error: {e}"

def process_images(input_dir, output_dir, target_size, naming_prefix):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            yield f"Made folder '{output_dir}'"
        
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'heic'))]
        total = len(image_files)

        if total == 0:
            yield "There are no images to process."
            return
        
        for i, filename in enumerate(image_files):
            try:
                input_path = os.path.join(input_dir, filename)
                img = Image.open(input_path)

                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

                new_filename = f"{naming_prefix}_{str(i + 1).zfill(4)}.jpg"
                output_path = os.path.join(output_dir, new_filename)

                resized_img.save(output_path, quality=95)

                yield f"The Conversion is complete: ({i + 1}/{total}) {filename} -> {new_filename}"
            
            except Exception as e:
                yield f"Error: {filename} - {e}"

        yield "All image processing has been completed."

    except FileNotFoundError:
        yield f"Error: Can't find {input_dir}."
    except Exception as e:
        yield f"Critical error: {e}"