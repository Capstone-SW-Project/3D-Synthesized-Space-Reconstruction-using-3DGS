#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <folder_name> <scale> <removal_json_file>"
    exit 1
fi

FOLDER_NAME="$1"
SCALE="$2"
REMOVAL_JSON_FILE="$3"

# 1. Preprocess to make proper images for input (Optional)
echo "Step 1: Preprocessing images..."
# python make_img.py                        # Video 파일이 있는 경우
# python img_resize.py                      # Image 크기가 너무 커서 COLMAP을 돌릴 때 시간이 오래 걸리는 경우
# python convert.py -s "$FOLDER_NAME"       # convert initial camera pose and point cloud with colmap

# 2. Make segmented images and find index of target objects
echo "\nStep 2: Preparing pseudo labels..."
bash script/prepare_pseudo_label.sh "$FOLDER_NAME" "$SCALE"

# 3. Train
echo "\nStep 3: Training the model..."
bash script/train.sh "$FOLDER_NAME" "$SCALE"

# 4. Choose removal operation (object or background)
echo "\nStep 4: Choosing removal operation..."
# 객체 제거
# bash script/edit_object_removal.sh "output/$FOLDER_NAME" "config/object_removal/$REMOVAL_JSON_FILE"
# 배경 제거
bash script/edit_background_removal.sh "output/$FOLDER_NAME" "config/object_removal/$REMOVAL_JSON_FILE"

# 5. Remove artifacts in pointcloud file which background (object) is removed by step 4
echo "\nStep 5: Removing artifacts..."
bash script/edit_artifact.sh "$FOLDER_NAME"

echo "\nAll steps completed successfully."
