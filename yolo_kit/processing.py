import os
from PIL import Image

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