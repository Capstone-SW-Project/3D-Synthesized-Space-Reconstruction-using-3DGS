# Capstone-SW-Project
2024 졸업 프로젝트 - 3DGS를 이용한 Point Cloud 합성

Professor : 이성윤 교수님\
Co-worker : 박현준, 임도현

> 최신 Computer Vision 기술인 3D Gaussian Splatter를 이용하여 서로 다른 배경에 존재하고 있는 Object들을 3DGS로 렌더링한 뒤 이들의 Point Cloud들을 합성해서 3D Space에 Reconstruct 하는 프로젝트입니다.

- Environment Setting : [EnvSetting.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/Env_Setting.md)
- Implementation detail : [Implement.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/Implement.md)

## COLMAP

|한양대학교|혼천의|세종대왕|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/COLMAP/hanyang.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/COLMAP/clock.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/COLMAP/sejong.jpg)|

## Point Cloud

|Wide-view|Front|Rear|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/pointcloud1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/pointcloud2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/pointcloud3.jpg)|

## Rendering

### Images

|한양대|+|혼천의|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/clock1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/clock2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/clock4.jpg)|
|한양대|+ 혼천의|+ 세종대왕|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/result1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/result2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/result3.jpg)|

### GIF

|한양대학교|혼천의|세종대왕|결과물|
|:--:|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/rendering_gif/hanyang.gif)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/rendering_gif/clock.gif)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/rendering_gif/sejong.gif)|![4](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/rendering_gif/synth_result.gif)|
