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
최신 Computer Vision 기술인 3D Gaussian Splatting을 이용하여 서로 다른 배경에 존재하고 있는 Object들을 3DGS로 렌더링한 뒤 이들의 Point Cloud들을 합성해서 3D Space에 Reconstruct 하는 프로젝트입니다.

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
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/3gds_process.png)

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

### Analysis
<Gaussian Grouping>
[장점]
- Image 약 150~200 장으로 3D Space를 복원할 수 있다.
- Gaussian Grouping의 경우 SAM을 이용하여 index 값을 부여한 뒤, 그 index 값을 이용하여 Gaussian들을 Clustering 하는 과정을 통해 객체 또는 배경을 제거할 수 있다.
- 객체를 지운 영역을 inpainting을 통해 원래 그 위치에 객체가 없었던 것 처럼 자연스럽게 복원할 수 있다.
- Style transfer를 통해 특정 객체를 원하는 모습으로 변환할 수 있다.

[단점]
- 촬영하고자 하는 대상의 크기가 너무 커서 위쪽을 촬영하지 못할 경우, Rendering 했을 때 Quality가 떨어진다.
- Index 값을 올바르게 넣지 않을 경우 원하지 않는 부분이 Grouping 되거나, Masking 영역이 제대로 제거 되지 않아 수 많은 artifact들이 생기게 된다
- 다양한 각도로 촬영을 해야 보다 정확한 객체 분리가 가능하다

### Discussion

---

## 6.Conclusion

---

## 7.References
1. Schonberger, Johannes L., and Jan-Michael Frahm. "Structure-from-motion revisited." Proceedings of the IEEE conference on computer vision and pattern recognition. 2016.
2. Kerbl, Bernhard, et al. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." ACM Trans. Graph. 42.4 (2023): 139-1.
3. Ye, Mingqiao, et al. "Gaussian Grouping: Segment and Edit Anything in 3D Scenes." arXiv preprint arXiv:2312.00732 (2023).
4. Shijie Zhou, et al. "Feature 3DGS: Supercharging 3D Gaussian Splatting to Enable Distilled Feature Fields." Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024, pp. 21676-21685
5. Alexander Kirillov, et al. "Segment Anything." Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2023, pp. 4015-4026
