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
- Environment Setting : [EnvSetting.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/Env_Setting.md)
- Implementation detail : [Implement.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/Implement.md)

---

## 3. Methodology

#### COLMAP 3D Reconstruction Process
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/methodology_images/colmap_process.png)

##### Images
- 여러장의 이미지 입력

##### 1) Correspondence Search (대응점 검색)

###### 1-1) Feature Extraction (특징점 추출)
- **Input**: 이미지 집합 \( I = \{ I_i | i = 1, \dots, N_1 \} \)
- **Process**: SIFT 기법을 이용하여 각 이미지에서 특징점 추출
- **Output**: 각 이미지에 대한 로컬 특징 \( F_i = \{ (X_j, f_j) | j = 1, \dots, N_{F_i} \} \), 여기서 \( X_j \)는 2차원 위치

###### 1-2) Feature Matching (특징점 매칭)
- **Input**: 추출된 특징점 집합 \( F_i \)
- **Process**: 추출한 특징점을 바탕으로 각 이미지 쌍에서 같은 장면 부분을 찾아서 잠재적으로 겹치는 이미지 쌍을 매칭
- **Output**: 잠재적으로 겹치는 이미지 쌍 집합 \( C = \{ \{ I_a, I_b \} | I_a, I_b \in I, a < b \} \)

###### 1-3) Geometric Verification (기하학적 검증)
- **Input**: 매칭된 이미지 쌍 집합 \( C \)
- **Process**: 기하학적 검증을 통해 Inlier 대응점 및 이미지 쌍 간의 기하학적 관계를 확인
- **Output**: 기하학적으로 검증된 이미지 쌍 \( C^ \), Inlier 대응점 \( M^_{ab} \), 이미지 쌍 간의 기하학적 관계 \( G_{ab} \)

##### 2) Incremental Reconstruction (점진적 재구성)

###### 2-1) Initialization (초기화)
- **Input**: Scene Graph
- **Process**: 초기 이미지 두 개를 선택하여 초기화 (겹치는 영역이 많은 이미지나 드문드문 겹치는 이미지를 선택)
- **Output**: 초기화된 이미지 쌍 및 관련 카메라 포즈

###### 2-2) Image Registration (이미지 등록)
- **Input**: 초기화된 이미지 쌍
- **Process**: 새로운 이미지를 추가하면서, 해당 이미지의 포즈(위치 및 방향)를 추정
- **Output**: 등록된 이미지와 카메라 포즈

###### 2-3) Triangulation (삼각측량)
- **Input**: 등록된 이미지와 카메라 포즈
- **Process**: 여러 이미지에서 공통으로 관측된 특징점들을 이용해 3D 위치를 추정하여 포인트 클라우드를 생성
- **Output**: 포인트 클라우드 (초기 구조)

###### 2-4) Bundle Adjustment (번들 조정)
- **Input**: 등록된 카메라 포즈와 포인트 클라우드
- **Process**: 카메라 파라미터 \( P \)와 포인트 \( X \)를 최적화하여 reprojection error를 최소화
- **Output**: 카메라 포즈 추정 \( P = \{ P_c | c = 1, \dots, N_p \} \)와 3D 포인트 구조 \( X = \{ X_k | k = 1, \dots, N_x \} \)

###### 2-5) Outlier Filtering (이상치 제거)
- **Input**: 번들 조정 후 포인트 클라우드
- **Process**: 잘못된 매칭이나 노이즈로 인해 발생한 Outliers를 제거하여 구조를 정제
- **Output**: Outliers가 제거된 정제된 포인트 클라우드

##### Reconstruction (재구성 결과)
- 최종적으로 3D 구조를 재구성하여 포인트 클라우드를 얻는다.

---

##### 3D Gaussian Splatting Process Overview
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/methodology_images/3gds_process.png)

##### 1. Initialization
- **Input**: SfM(COLMAP)에서 얻은 카메라 포즈와 포인트 클라우드
- **Output**: 3D Gaussian 분포
- **Description**: COLMAP 등의 SfM 방법을 통해 얻은 카메라 포즈와 포인트 클라우드를 기반으로 3D Gaussian 분포를 초기화합니다.

##### 2. Projection
- **Process**: 3D Gaussian을 이미지 평면(Image Plane)으로 투영
- **Purpose**: 투영된 결과를 GT(Ground Truth) 이미지와 비교하여 파라미터를 업데이트하기 위함
- **Description**: 각 3D Gaussian이 카메라 뷰를 기준으로 2D 이미지 평면에 투영됩니다. 이 투영된 이미지가 이후 Loss 계산의 기준이 됩니다.

##### 3. Differentiable Tile Rasterizer
- **Process**: Differentiable한 Tile Rasterization을 통해 2D Gaussian들을 하나의 이미지로 생성
- **Output**: Rasterized 2D 이미지
- **Description**: Differentiable Tile Rasterizer는 투영된 Gaussian들을 하나의 2D 이미지로 합성하여 최종적으로 모델이 생성한 이미지를 출력합니다. 이 과정은 미분 가능하므로 최적화에 사용됩니다.

##### 4. Gradient Flow
- **Process**: 생성된 이미지와 GT 이미지 사이의 Loss를 계산하고, Loss에 따른 Gradient를 전파
- **Description**: Loss를 통해 계산된 Gradient를 역전파하여 각 파라미터가 업데이트될 수 있도록 합니다. 이는 모델이 GT 이미지에 더 가깝게 학습되도록 합니다.

##### 5. Adaptive Density Control
- **Process**: Gradient에 기반하여 Gaussian 형태를 변환
- **Description**: Gradient를 기반으로 각 Gaussian의 형태(위치, 크기, 밀도 등)를 조정하여 최적화합니다. 이를 통해 Gaussian이 GT 이미지와 일치하는 방향으로 업데이트됩니다.

##### Summary
이 과정은 COLMAP으로부터 얻은 초기 3D 정보를 바탕으로 3D Gaussian을 학습하고, GT 이미지와 비교하여 최적화하는 과정입니다. 최종적으로 Loss에 따른 Gradient가 각 단계로 전파되면서 Gaussian 분포가 GT에 가깝게 조정됩니다.

---

## 4.Results
### COLMAP

|한양대학교|혼천의|세종대왕|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/COLMAP/hyu.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/COLMAP/clk.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/result_images/COLMAP/king.jpg)|


#### Point Cloud

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

---

## 5.Analysis and Discussion

---

## 6.Conclusion

---

## 7.References
1. Schonberger, Johannes L., and Jan-Michael Frahm. "Structure-from-motion revisited." Proceedings of the IEEE conference on computer vision and pattern recognition. 2016.
2. Kerbl, Bernhard, et al. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." ACM Trans. Graph. 42.4 (2023): 139-1.
3. Ye, Mingqiao, et al. "Gaussian grouping: Segment and edit anything in 3d scenes." arXiv preprint arXiv:2312.00732 (2023).