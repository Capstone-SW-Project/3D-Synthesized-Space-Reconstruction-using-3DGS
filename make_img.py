# 동영상을 불러와서 frame 단위로 잘라서 image 여러 장으로 저장하는 코드 #

import cv2
import os

# 비디오 파일 경로
video_path = 'input_video.mp4'  
folder_name = input("Enter the folder name: ")
output_folder = f'output_frames/{folder_name}'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 비디오 정보 확인
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = 0

# 프레임 추출 간격 설정
frame_interval = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # frame_interval 간격으로 이미지 저장
    if frame_count % frame_interval == 0:
        cv2.imwrite(os.path.join(output_folder, f'frame_{frame_count:04d}.jpg'), frame)
        
    frame_count += 1

cap.release()
print(f'총 {frame_count//frame_interval}개의 프레임 저장 완료.')