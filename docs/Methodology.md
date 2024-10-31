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

---

# Summary

- 이 과정은 COLMAP으로부터 얻은 초기 3D 정보를 바탕으로 3D Gaussian을 학습하고, GT 이미지와 비교하여 최적화하는 과정입니다. 최종적으로 Loss에 따른 Gradient가 각 단계로 전파되면서 Gaussian 분포가 GT에 가깝게 조정됩니다.

## Gaussian Grouping Process

### 1. 2D Image and Mask Input

- **Input**: Multiview 2D 이미지 (Ground Truth 이미지)
- **SAM**:
  - **Input**: Multiview 2D 이미지
  - **Output**: 2D 마스크 (m)

### 2. Identity Consistency across Views

- **Zero-shot Tracker**: 시점 간 아이덴티티 일관성을 유지하기 위해 마스크 연관(Mask Association)을 수행합니다.
  - **Input**: SAM에서 생성한 2D Mask (m)와 Camera Pose
  - **Output**: 3D Object Identity Mask $\hat{M}$

### 3. 3D Gaussian Rendering and Grouping

- **Identity Encoding**: 객체의 인스턴스 ID로 작용하여 각 3D 객체를 구분하는 데 사용됩니다.
- **$E_{id}$**: 2D Image plane의 각 픽셀에 대한 Identity Feature으로, 해당 픽셀이 어떤 객체에 속하는지를 나타냅니다.

1. **Projection from 3D to 2D**:
   - 3D Covariance Matrix ($\Sigma_{3D}$)을 2D로 투영하여 다음과 같이 변환합니다:

     ![Covariance]()

2. **2D 이미지에서 픽셀별 특징 계산**:
   - 각 픽셀의 Identity feature $E_{id}$는 다음과 같이 계산됩니다:
    
    ![Identity]()

   - **참고**: E_id는 2D 이미지의 각 픽셀에서 계산된 Identity Feature으로, 픽셀이 어떤 객체에 속하는지를 나타냅니다.

### 4. Grouping Loss

- **Input**: 2D 이미지 평면의 각 픽셀에 대한 Identity Feature $E_{id}$

1. **2D Identity Loss (L_2D)**:
   - $E_{id}$를 MLP에 통과시키고 SoftMax 연산을 적용하여 각 픽셀이 K개의 카테고리(객체 클래스) 중 하나에 속하도록 분류합니다.

2. **3D Identity Loss (L_3D)**:
   - KL Divergence를 사용하여 동일 객체에 속하는 가우시안들이 유사한 E_id 값을 가지도록 하여 아이덴티티 인코딩의 일관성을 유지합니다.
   
     ![loss]

3. **Final Loss (L_render)**:
   - 재구성 손실과 아이덴티티 손실을 결합하여 최종 손실을 계산합니다:
   
     ![Final]()


## Summary of Process

- **Multiview 2D Image**는 **SAM**을 통해 **2D 마스크**로 변환됩니다.
- **Zero-shot Tracker**는 이러한 마스크와 카메라 포즈를 사용하여 시점 간에 일관된 **3D Object Identity Mask** $\hat{M}$를 생성합니다.
- **3D Gaussian Rendering**을 수행하여 가우시안을 2D 공간으로 투영하고 각 픽셀의 Identity Feature (E_id)을 계산합니다.
- **Grouping Loss**를 적용하여 아이덴티티 일관성을 최적화하며, 2D 및 3D 아이덴티티 손실을 활용합니다.
- **Final Loss**는 재구성 손실과 아이덴티티 손실을 결합하여 3D 객체 그룹핑의 일관성을 보장합니다.
