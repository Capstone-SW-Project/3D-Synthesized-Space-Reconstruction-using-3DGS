import os
import numpy as np
from PIL import Image
import argparse
from tqdm import tqdm


# Image를 읽어오는 함수
def read_image(image_path):
    image = Image.open(image_path)
    return np.array(image)

# Image array와 foreground indices를 받아서 binary mask를 생성하는 함수
def generate_binary_mask(image_array, foreground_indices):
    binary_mask = np.zeros_like(image_array, dtype=np.uint8)
    for index in foreground_indices:
        binary_mask[image_array == index] = 1 
    return binary_mask

# Binary mask를 저장하는 함수
def save_binary_mask(binary_mask, output_path):
    mask_image = Image.fromarray(binary_mask * 255)
    mask_image.save(output_path)

# 폴더 내의 모든 이미지에 대해 binary mask를 생성하고 저장하는 함수
def process_images_in_folder(folder_path, output_folder, foreground_indices):
    os.makedirs(output_folder, exist_ok=True)
    
    image_files = [
        filename for filename in os.listdir(folder_path)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    
    for filename in tqdm(image_files, desc="Processing binary masks"):
        image_path = os.path.join(folder_path, filename)
        image_array = read_image(image_path)

        # Generate binary mask
        binary_mask = generate_binary_mask(image_array, foreground_indices)

        # Save binary mask
        output_path = os.path.join(output_folder, f"mask_{filename}")
        save_binary_mask(binary_mask, output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate binary masks based on selected indices.")
    parser.add_argument('-d', '--dataset', type=str, required=True, help='Dataset name')
    parser.add_argument('-i', '--indices', type=str, required=True, help='Comma-separated list of indices')
    
    args = parser.parse_args()
    
    dataset_name = args.dataset
    foreground_indices = list(map(int, args.indices.split(',')))
    
    folder_path = f'data/{dataset_name}/object_mask'
    output_folder = f'data/{dataset_name}/new_mask'
    
    process_images_in_folder(folder_path, output_folder, foreground_indices)


if __name__ == "__main__":
    main()
