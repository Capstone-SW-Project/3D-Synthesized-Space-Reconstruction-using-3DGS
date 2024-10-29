# 🎓Capstone-SW-Project
2024 졸업 프로젝트 - 3D Gaussian Splatter를 이용한 Point Cloud 합성

Professor : 이성윤 교수님\
Co-worker : 박현준, 임도현

---

## Table of Contents
1. Objective 
2. Environment and Implementation
3. Methodology
4. Results
5. Analysis and Discussion
6. Conclusion
7. References

---

## 1. Objective
> 최신 Computer Vision 기술인 3D Gaussian Splatter를 이용하여 서로 다른 배경에 존재하고 있는 Object들을 3DGS로 렌더링한 뒤 이들의 Point Cloud들을 합성해서 3D Space에 Reconstruct 하는 프로젝트입니다.

---

## 2. Environment and Implementation
- Environment Setting : [EnvSetting.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/markdown/Env_Setting.md)
- Implementation detail : [Implement.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/markdown/Implement.md)

---

## 3. Methodology

#### COLMAP 3D Reconstruction Process
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/colmap_process.png)

##### Images
- 여러 이미지 입력

##### 1) Correspondence Search (대응점 검색)

###### 1-1) Feature Extraction (특징점 추출)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/FeatureExtraction.png)

###### 1-2) Feature Matching (특징점 매칭)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/FeatureMatching.png)

###### 1-3) Geometric Verification (기하학적 검증)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/GeometricVerification.png)


##### 2) Incremental Reconstruction (점진적 재구성)

###### 2-1) Initialization (초기화)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/Initialization.png)


###### 2-2) Image Registration (이미지 등록)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/ImageRegistration.png)

###### 2-3) Triangulation (삼각측량)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/Triangulation.png)


###### 2-4) Bundle Adjustment (번들 조정)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/BA.png)


###### 2-5) Outlier Filtering (이상치 제거)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/OutlierFiltering.png)


##### Reconstruction (재구성 결과)
- 최종적으로 3D 구조를 재구성하여 포인트 클라우드를 얻는다.

---

##### 3D Gaussian Splatting Process Overview
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology_images/3gds_process.png)

##### 1. Initialization
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/Initialization.png)


##### 2. Projection
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/Projection.png)


##### 3. Differentiable Tile Rasterizer
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/DifferentiableTileRasterizer.png)


##### 4. Gradient Flow
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/GradientFlow.png)


##### 5. Adaptive Density Control
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/AdaptiveDensityControl.png)


##### Summary
- 이 과정은 COLMAP으로부터 얻은 초기 3D 정보를 바탕으로 3D Gaussian을 학습하고, GT 이미지와 비교하여 최적화하는 과정입니다. 최종적으로 Loss에 따른 Gradient가 각 단계로 전파되면서 Gaussian 분포가 GT에 가깝게 조정됩니다.
---

## 4.Results
### COLMAP

|한양대학교|혼천의|세종대왕|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/COLMAP/hyu.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/COLMAP/clk.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/COLMAP/king.jpg)|


#### Point Cloud

|Wide-view|Front|Rear|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/pointcloud1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/pointcloud2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/pointcloud3.jpg)|

## Rendering

### Images

|한양대|+|혼천의|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/clock1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/clock2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/clock4.jpg)|
|한양대|+ 혼천의|+ 세종대왕|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/result1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/result2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/result/result3.jpg)|

### GIF

|한양대학교|혼천의|세종대왕|결과물|
|:--:|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/rendering/hanyang.gif)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/rendering/clock.gif)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/rendering/sejong.gif)|![4](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/rendering/synth_result.gif)|

---

## 5.Analysis and Discussion

---

## 6.Conclusion

---

## 7.References
1. Schonberger, Johannes L., and Jan-Michael Frahm. "Structure-from-motion revisited." Proceedings of the IEEE conference on computer vision and pattern recognition. 2016.
2. Kerbl, Bernhard, et al. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." ACM Trans. Graph. 42.4 (2023): 139-1.
3. Ye, Mingqiao, et al. "Gaussian grouping: Segment and edit anything in 3d scenes." arXiv preprint arXiv:2312.00732 (2023).
