# 이미지 크기가 너무 클 경우 COLMAP을 돌릴 때 시간이 오래 걸리기 때문에
# 1000x1000으로 resize해 주는 것이 좋다.

import cv2
import glob
import os

imgpath = 'C:/Users/CV/Desktop/3DGS/south-building/images'
savepath = 'C:/Users/CV/Desktop/3DGS/south-building/resized_images'

if not os.path.exists(savepath):
    os.makedirs(savepath)

filename_list = sorted(glob.glob(os.path.join(imgpath, '*.[jp][pn]g')))

for i, filename in enumerate(filename_list):
    img = cv2.imread(filename)
    height, width = img.shape[:2]

    if max(height, width) > 3000:
        scale = 1000 / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    name = os.path.basename(filename)
    
    output_path = os.path.join(savepath, name)
    cv2.imwrite(output_path, img)
    
    print(f"처리된 이미지 {i+1}/{len(filename_list)}: {name}")

print("모든 이미지 처리 완료.")