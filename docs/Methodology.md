# Methodology

## COLMAP 3D Reconstruction Process
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/colmap_process.png)

### Images
- 여러 이미지 입력

### 1) Correspondence Search (대응점 검색)

#### 1-1) Feature Extraction (특징점 추출)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/FeatureExtraction.png)

#### 1-2) Feature Matching (특징점 매칭)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/FeatureMatching.png)

#### 1-3) Geometric Verification (기하학적 검증)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/GeometricVerification.png)


### 2) Incremental Reconstruction (점진적 재구성)

#### 2-1) Initialization (초기화)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/Initialization.png)


#### 2-2) Image Registration (이미지 등록)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/ImageRegistration.png)

#### 2-3) Triangulation (삼각측량)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/Triangulation.png)


#### 2-4) Bundle Adjustment (번들 조정)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/BA.png)


#### 2-5) Outlier Filtering (이상치 제거)
![COLMAP_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/colmap/OutlierFiltering.png)


## Reconstruction (재구성 결과)
- 최종적으로 3D 구조를 재구성하여 포인트 클라우드를 얻는다.

---

## 3D Gaussian Splatting Process Overview
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/3gds_process.png)

### 1. Initialization
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/Initialization.png)


### 2. Projection
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/Projection.png)


### 3. Differentiable Tile Rasterizer
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/DifferentiableTileRasterizer.png)


### 4. Gradient Flow
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/GradientFlow.png)


### 5. Adaptive Density Control
![3GDs_PROCESS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/LaTeX/3gds/AdaptiveDensityControl.png)