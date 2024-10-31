# Methodology

#### COLMAP 3D Reconstruction Process
![colmap](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/colmap_process.png)
##### Images
- 여러 이미지 입력

---

##### 1) Correspondence Search (대응점 검색)

###### 1-1) Feature Extraction (특징점 추출)
- **Input**: 이미지 집합 $$\( I = \{ I_i | i = 1, \dots, N_1 \} \)$$
- **Process**: SIFT 기법을 이용하여 각 이미지에서 특징점 추출
- **Output**: 각 이미지에 대한 로컬 특징 $$\( F_i = \{ (X_j, f_j) | j = 1, \dots, N_{F_i} \} \)$$, 여기서 $$\( X_j \)$$ 는 2차원 위치

---

###### 1-2) Feature Matching (특징점 매칭)
- **Input**: 추출된 특징점 집합 $$\( F_i \)$$
- **Process**: 추출한 특징점을 바탕으로 각 이미지 쌍에서 같은 장면 부분을 찾아서 잠재적으로 겹치는 이미지 쌍을 매칭
- **Output**: 잠재적으로 겹치는 이미지 쌍 집합 $$\( C = \{ \{ I_a, I_b \} | I_a, I_b \in I, a < b \} \)$$

---

###### 1-3) Geometric Verification (기하학적 검증)
- **Input**: 매칭된 이미지 쌍 집합 $$\( C \)$$
- **Process**: 기하학적 검증을 통해 Inlier 대응점 및 이미지 쌍 간의 기하학적 관계를 확인
- **Output**: 기하학적으로 검증된 이미지 쌍 $$\( \hat {C} \)$$, Inlier 대응점 $$\(\hat {M}_{ab}\)$$, 이미지 쌍 간의 기하학적 관계 $$\(G_{ab}\)$$

---

##### 2) Incremental Reconstruction (점진적 재구성)

###### 2-1) Initialization (초기화)
- **Input**: Scene Graph
- **Process**: 초기 이미지 두 개를 선택하여 초기화 (겹치는 영역이 많은 이미지나 드문드문 겹치는 이미지를 선택)
- **Output**: 초기화된 이미지 쌍 및 관련 카메라 포즈

---

###### 2-2) Image Registration (이미지 등록)
- **Input**: 초기화된 이미지 쌍
- **Process**: 새로운 이미지를 추가하면서, 해당 이미지의 포즈(위치 및 방향)를 추정
- **Output**: 등록된 이미지와 카메라 포즈

---

###### 2-3) Triangulation (삼각측량)
- **Input**: 등록된 이미지와 카메라 포즈
- **Process**: 여러 이미지에서 공통으로 관측된 특징점들을 이용해 3D 위치를 추정하여 포인트 클라우드를 생성
- **Output**: 포인트 클라우드 (초기 구조)

---

###### 2-4) Bundle Adjustment (번들 조정)
- **Input**: 등록된 카메라 포즈와 포인트 클라우드
- **Process**: 카메라 파라미터 $$\( P \ )$$ 와 포인트 $$\( X \)$$를 최적화하여 reprojection error를 최소화
- **Output**: 카메라 포즈 추정 $$\( P = \{ P_c | c = 1, \dots, N_p \} \)$$와 3D 포인트 구조 $$\( X = \{ X_k | k = 1, \dots, N_x \} \)$$

---

###### 2-5) Outlier Filtering (이상치 제거)
- **Input**: 번들 조정 후 포인트 클라우드
- **Process**: 잘못된 매칭이나 노이즈로 인해 발생한 Outliers를 제거하여 구조를 정제
- **Output**: Outliers가 제거된 정제된 포인트 클라우드

---

##### Reconstruction (재구성 결과)
- 최종적으로 3D 구조를 재구성하여 포인트 클라우드를 얻는다.

---
##### 3D Gaussian Splatting Process Overview

---

##### 1. Initialization
- **Input**: SfM(COLMAP)에서 얻은 카메라 포즈와 포인트 클라우드
- **Output**: 3D Gaussian 분포  
$$Σ^{3D}= RSS^TR^T$$
- **Description**: COLMAP 등의 SfM 방법을 통해 얻은 카메라 포즈와 포인트 클라우드를 기반으로 3D Gaussian 분포를 초기화합니다.

---

##### 2. Projection
- **Process**: 3D Gaussian을 이미지 평면(Image Plane)으로 투영
- **Purpose**: 투영된 결과를 GT(Ground Truth) 이미지와 비교하여 파라미터를 업데이트하기 위함  
$$Σ^{2D}= JW Σ^{3D}W^TJ^T$$
- **Description**: 각 3D Gaussian이 카메라 뷰를 기준으로 2D 이미지 평면에 투영됩니다. 이 투영된 이미지가 이후 Loss 계산의 기준이 됩니다.

---

##### 3. Differentiable Tile Rasterizer
- **Process**: Differentiable한 Tile Rasterization을 통해 2D Gaussian들을 하나의 이미지로 생성
- **Output**: Rasterized 2D 이미지
- **Description**: Differentiable Tile Rasterizer는 투영된 Gaussian들을 하나의 2D 이미지로 합성하여 최종적으로 모델이 생성한 이미지를 출력합니다. 이 과정은 미분 가능하므로 최적화에 사용됩니다.

---

##### 4. Gradient Flow
- **Process**: 생성된 이미지와 GT 이미지 사이의 Loss를 계산하고, Loss에 따른 Gradient를 전파  
$$L = (1 - \lambda) L_1 + \lambda L_{D\text{-}SSIM}$$
- **Description**: Loss를 통해 계산된 Gradient를 역전파하여 각 파라미터가 업데이트될 수 있도록 합니다. 이는 모델이 GT 이미지에 더 가깝게 학습되도록 합니다.

---

##### 5. Adaptive Density Control
- **Process**: Gradient에 기반하여 Gaussian 형태를 변환  
![adaptive](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/adaptive.png)  
- **Description**: Gradient를 기반으로 각 Gaussian의 형태(위치, 크기, 밀도 등)를 조정하여 최적화합니다. 이를 통해 Gaussian이 GT 이미지와 일치하는 방향으로 업데이트됩니다.

---

##### Summary
이 과정은 COLMAP으로부터 얻은 초기 3D 정보를 바탕으로 3D Gaussian을 학습하고, GT 이미지와 비교하여 최적화하는 과정입니다. 최종적으로 Loss에 따른 Gradient가 각 단계로 전파되면서 Gaussian 분포가 GT에 가깝게 조정됩니다.

## Gaussian Grouping Process

### 1. 2D Image and Mask Input

- **Input**: Multiview 2D 이미지 (Ground Truth 이미지)
- **SAM**:
  - **Input**: Multiview 2D 이미지
  - **Output**: 2D 마스크 (m)

### 2. Identity Consistency across Views

- **Zero-shot Tracker**: 시점 간 아이덴티티 일관성을 유지하기 위해 마스크 연관(Mask Association)을 수행합니다.
  - **Input**: SAM에서 생성한 2D Mask (m)와 Camera Pose
  - **Output**: 3D Object Identity Mask $$\hat{M}$$

### 3. 3D Gaussian Rendering and Grouping

- **Identity Encoding**: 객체의 인스턴스 ID로 작용하여 각 3D 객체를 구분하는 데 사용됩니다.
- **$E_{id}$**: 2D Image plane의 각 픽셀에 대한 Identity Feature으로, 해당 픽셀이 어떤 객체에 속하는지를 나타냅니다.

1. **Projection from 3D to 2D**:
   - 3D Covariance Matrix ($\Sigma_{3D}$)을 2D로 투영하여 다음과 같이 변환합니다:  
      $$Σ^{2D}= JW Σ^{3D} W^TJ^T$$ 

2. **2D 이미지에서 픽셀별 특징 계산**:
   - 각 픽셀의 Identity feature $E_{id}$는 다음과 같이 계산됩니다:  
    $$E_{\text{id}} = \sum_{i \in \mathcal{N}} e_i \alpha'_i \prod{j=1}^{i-1} (1 - \alpha'_j)$$  
    where,  $$\alpha'_i(x) = \exp \left( - \frac{1}{2} (x - \mu_i)^T (\Sigma^{2D})^{-1} (x - \mu_i) \right)$$  

   - **참고**: $$E_{\text {id}}$$는 2D 이미지의 각 픽셀에서 계산된 Identity Feature으로, 픽셀이 어떤 객체에 속하는지를 나타냅니다.

### 4. Grouping Loss

- **Input**: 2D 이미지 평면의 각 픽셀에 대한 Identity Feature $E_{id}$

1. **2D Identity Loss (L_2D)**:
   - $$E_{id}$$를 MLP에 통과시키고 SoftMax 연산을 적용하여 각 픽셀이 K개의 카테고리(객체 클래스) 중 하나에 속하도록 분류합니다.

2. **3D Identity Loss (L_3D)**:
   - KL Divergence를 사용하여 동일 객체에 속하는 가우시안들이 유사한 E_id 값을 가지도록 하여 아이덴티티 인코딩의 일관성을 유지합니다.  
    $$L_{3d} = \frac{1}{m} \sum{j=1}^{m} D_{\text{KL}}(P \parallel Q) = \frac{1}{mk} \sum_{j=1}^{m} \sum_{i=1}^{k} F(e_j) \log \left( \frac{F(e_j)}{F(e_i')} \right)$$

3. **Final Loss (L_render)**:
   - 재구성 손실과 아이덴티티 손실을 결합하여 최종 손실을 계산합니다:  
    $$L_{{render}} = L_{\text{rec}} + L_{\text{id}} = L_{\text{rec}} + \lambda_{\text{2d}} L_{\text{2d}} + \lambda_{\text{3d}} L_{\text{3d}}$$  
     ![loss](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/grouping.png)



## Summary of Process

- **Multiview 2D Image**는 **SAM**을 통해 **2D 마스크**로 변환됩니다.
- **Zero-shot Tracker**는 이러한 마스크와 카메라 포즈를 사용하여 시점 간에 일관된 **3D Object Identity Mask** $\hat{M}$를 생성합니다.
- **3D Gaussian Rendering**을 수행하여 가우시안을 2D 공간으로 투영하고 각 픽셀의 Identity Feature (E_id)을 계산합니다.
- **Grouping Loss**를 적용하여 아이덴티티 일관성을 최적화하며, 2D 및 3D 아이덴티티 손실을 활용합니다.
- **Final Loss**는 재구성 손실과 아이덴티티 손실을 결합하여 3D 객체 그룹핑의 일관성을 보장합니다.
