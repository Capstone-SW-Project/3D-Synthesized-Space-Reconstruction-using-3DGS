import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
import random
import time

def read_image(image_path):
    image = Image.open(image_path)
    return np.array(image)


def get_unique_indices(image_array):
    return np.unique(image_array)


def create_index_overlay_image(image_array, output_path):
    unique_indices = get_unique_indices(image_array)
    height, width = image_array.shape

    overlay_image = Image.fromarray(image_array).convert("RGB")
    draw = ImageDraw.Draw(overlay_image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()
    
    index_colors = {index: (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                    for index in unique_indices}
    
    for index in unique_indices:
        if index == 0:  # Skip background index
            continue
        
        positions = np.argwhere(image_array == index)
        if positions.size == 0:
            continue
        
        # Bounding box 좌표값 얻기
        y_min, x_min = positions.min(axis=0)
        y_max, x_max = positions.max(axis=0)
        
        # Bounding box 그리기
        color = index_colors[index]
        draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=3)
        
        text_position = (x_min + 5, y_min + 5)
        text = str(index)
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Index 값을 적을 text box를 bounding box 위에 생성
        draw.rectangle([text_position, (text_position[0] + text_width + 4, text_position[1] + text_height + 4)],
                       fill='black')
        
        draw.text(text_position, text, fill="white", font=font)
    
    overlay_image.save(output_path)
    print(f"Index overlay image saved: {output_path}")


def process_images(folder_path, overlay_folder):
    os.makedirs(overlay_folder, exist_ok=True)
    
    start_time = time.time()
    all_indices = set()
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            
            image_array = read_image(image_path)
            
            indices = get_unique_indices(image_array)
            all_indices.update(indices)
            
            overlay_output_path = os.path.join(overlay_folder, f"overlay_{filename}")
            create_index_overlay_image(image_array, overlay_output_path)
    
    end_time = time.time()
    print("All unique indices found:", sorted(all_indices))
    print(f"Total processing time: {end_time - start_time:.2f} seconds")


def main():
    parser = argparse.ArgumentParser(description="Find unique indices and create overlay images.")
    parser.add_argument('-d', '--dataset', type=str, required=True, help='Dataset name')
    args = parser.parse_args()
    
    dataset_name = args.dataset
    folder_path = f'data/{dataset_name}/object_mask'
    overlay_folder = f'data/{dataset_name}/overlay_mask'
    
    process_images(folder_path, overlay_folder)


if __name__ == "__main__":
    main()
