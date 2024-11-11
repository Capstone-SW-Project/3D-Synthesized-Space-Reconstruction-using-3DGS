# Methodology

## Incremental SfM (=COLMAP)

![colmap](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/colmap_process.png)

### 1) Correspondence Search (대응점 검색)

#### 1-1) Feature Extraction (특징점 추출)
- **Input**: 이미지 집합 $I=\lbrace I_i|i=1,...,N_1\rbrace$
- **Process**: SIFT 기법을 이용하여 각 이미지에서 특징점 추출
- **Output**: 각 이미지에 대한 로컬 특징 $F_i=\lbrace(X_i,f_j)|j=1,...,N_{F_i}\rbrace$, 여기서 $X_j$ 는 2차원 위치

#### 1-2) Feature Matching (특징점 매칭)
- **Input**: 추출된 특징점 집합 $F_i$
- **Process**: 추출한 특징점을 바탕으로 각 이미지 쌍에서 같은 장면 부분을 찾아서 잠재적으로 겹치는 이미지 쌍을 매칭
- **Output**: 잠재적으로 겹치는 이미지 쌍 집합 $\lbrace(I_a,I_b)=I_a,I_b\in I,a<b\rbrace$

#### 1-3) Geometric Verification (기하학적 검증)
- **Input**: 매칭된 이미지 쌍 집합 $$\( C \)$$
- **Process**: 기하학적 검증을 통해 Inlier 대응점 및 이미지 쌍 간의 기하학적 관계를 확인
- **Output**: 기하학적으로 검증된 이미지 쌍 $$\( \hat {C} \)$$, Inlier 대응점 $$\( M_{\text {ab}}\)$$, 이미지 쌍 간의 기하학적 관계 $$\(G_{\text ab}\)$$

---

### 2) Incremental Reconstruction (점진적 재구성)

#### 2-1) Initialization (초기화)
- **Input**: Scene Graph
- **Process**: 초기 이미지 두 개를 선택하여 초기화 (겹치는 영역이 많은 이미지나 드문드문 겹치는 이미지를 선택)
- **Output**: 초기화된 이미지 쌍 및 관련 카메라 포즈

##### 1. overlap 많이 되는(dense) 이미지 선택: 
overlap 되는 영역이 반복적으로 최적화되면서 좀 더 robust하고 accurate한 reconstruction 결과가 만들어진다.

##### 2. 빈도가 sparse한 이미지 선택: 
Bundle Adjustment 단계에서 반복적으로 처리할 feature가 줄어들어 reconstruction 성능은 낮아지나 전체적인 연산 시간이 줄어든다.

```python
      이미지1 ──── 이미지2
        │       ╱    │
        │      ╱     │
        │     ╱      │
      이미지3 ──── 이미지4
        
        ex) 이미지1과 이미지2는 기하학적으로 검증되어 있음
        ex) 이미지1과 이미지4는 기하학적으로 검증되어 있지 않음
```

#### 2-2) Image Registration (이미지 등록)
- **Input**: 초기화된 이미지 쌍
- **Process**: 새로운 이미지를 추가하면서, 해당 이미지의 포즈(위치 및 방향)를 추정
- **Output**: 등록된 이미지와 카메라 포즈

Initial image 2장의 카메라 pose를 World 좌표계로 등록함. 앞의 과정에서 이미 Feature matching이 되어 있으며, Geometric Verification 에서 상대 포즈와 intrinsic을 정보로 포함하고 있는 fundamental matrix가 이미 계산되어 있음. 따라서 이 matrix로 카메라 extrinsic과 intrinsic을 둘 다 구할 수 있다.

(*Extrinsic(카메라 외부 파라미터): 카메라 포즈(=위치&방향) *Intrinsic(카메라 내부 파라미터): 초점 거리나 렌즈 왜곡)

#### 2-3) Triangulation (삼각측량)
- **Input**: 등록된 이미지와 카메라 포즈
- **Process**: 여러 이미지에서 공통으로 관측된 특징점들을 이용해 3D 위치를 추정하여 포인트 클라우드를 생성
- **Output**: 포인트 클라우드 (초기 구조)

`Epipolar Geometry` 개념을 이용하여 Initial 3D Points 등록한다.  그 이후 새로 등록한 이미지의 3D Point들을 triangulation을 사용하여 이전에 등록한 3D Point들에 추가한다. 단, 이전에 등록된 3D Points들이 Image Registration이 잘됬다는 전제 하에 이뤄진다. (=새로운 이미지로 projection하면 관측됨)

이 과정은 반복 loop에서 stability를 증가시킨다.

#### 2-4) Bundle Adjustment (번들 조정)
- **Input**: 등록된 카메라 포즈와 포인트 클라우드
- **Process**: 카메라 파라미터 $$\( P \ )$$ 와 포인트 $$\( X \)$$를 최적화하여 reprojection error를 최소화
- **Output**: 카메라 포즈 추정 $(P=\lbrace P_c|c=1,\dots N_p\rbrace)$와 3D 포인트 구조 $(X=\lbrace X_k|k=1,\dots,N_x\rbrace)$

앞의 과정들을 보완하기 위해, 비선형 최적화를 추가적으로 수행한다.

아래 Reprojection error을 최소화하기 위해 카메라 parameter P와 point X를 non-linear refinement를 수행. pi는 projection 함수이고 rho는 outlier를 down-weight하기 위한 factor이다.

$E = \sum_j \rho_j \left( \| \pi(P_c, X_k) - X_j \|_2 \right)^2$

위 수식을 풀기 위해서 `Levenberg-Marquardt` 비선형 최적화 알고리즘 수행한다.

#### 2-5) Outlier Filtering (이상치 제거)
- **Input**: 번들 조정 후 포인트 클라우드
- **Process**: 잘못된 매칭이나 노이즈로 인해 발생한 Outliers를 제거하여 구조를 정제
- **Output**: Outliers가 제거된 정제된 포인트 클라우드

![PnP](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/PnP_Algo.png)

**PnP Algorithm** : 3D 공간에서의 점들의 위치와 해당 점들의 2D 이미지 내 위치를 기반으로 카메라 포즈를 추정하는데 사용된다.

이미 등록된 이미지들과의 feature corespondence를 사용하여 새로 등록되는 이미지에 대한 Camera Extrinsic을 추정하고 Intrinsic을 추정하여 Register한다.

---
## SAM (=Segment Anything Model)

### 1) SAM의 3요소

![SAM](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/SAM.png)

1. Prompt: 

    Promptable Segmentation
    
3. Model:
    
    $\text{Input}:$ prompt + image 
    $\text{output}:$ mask
    
4. Data:
    
    diverse & large-scale 학습

---

### 2) Model

![encoder](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/Encoder.png)

#### 2-1) Image Encoder (MAE Pretrained ViT)

![MAE](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/MAE_pretrained_ViT.png)

1. Split image into patches:
    
   - **Input**: image
   - **Output**: several patches
    
2. Random Masking: 마스킹 된 부분은 제거(즉, 모델은 일부 패치 만을 보고 학습함)
3. Encoder: 남은 패치는 ViT Encoder로 들어감
    
   - **Input**: survived patches
   - **Output**: embedding
    
4. Decoder: 전체 패치수, 동일한 길이와 출력 생성(마스킹 된 패치 정보를 재구성)
    
   - **Input**: embedding
   - **Output**: predicted image
    
5. Loss: MSE between GT and Predicted Image

#### 2-2) Prompt Encoder (Sparse or Dense)

1. Sparse: Points, boxes, text

   - Points or Boxes : Positional Encoding(위치를 저장함)을 합쳐 embedding 생성 
   - Text : CLIP의 text encoder 활용
    
2. Dense: masks
    
   - masks : Convolution 연산으로 embedding 생성하고 elemental wise하게 이미지와 합침

#### 2-3) Mask Decoder

   - **Input**: Image Embedding + Prompt Embedding
   - **Output**: mask

---

## 3D Gaussian Splatting

### 1) Process

![3DGS](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/3gds_process.png)

3D Gaussian Splatting은 SfM(Structure from Motion)으로부터 얻은 초기 3D 정보를 바탕으로 Gaussian 분포를 학습하여 이미지 생성 과정에서 활용하는 기법이다. 본 문서에서는 COLMAP을 사용하여 얻은 카메라 포즈와 포인트 클라우드 정보를 초기화하고, 최적화를 통해 GT(Ground Truth) 이미지에 가깝도록 조정하는 일련의 과정을 설명한다.

#### 1-1) Initialization

- **Input**: SfM(COLMAP)에서 얻은 카메라 포즈와 포인트 클라우드
- **Output**: 3D Gaussian 분포  

$$Σ^{3D}= RSS^TR^T$$

- **Description**: COLMAP 등의 SfM 방법을 통해 얻은 카메라 포즈와 포인트 클라우드를 기반으로 3D Gaussian 분포를 초기화합니다.

#### 1-2) Projection
- **Process**: 3D Gaussian을 이미지 평면(Image Plane)으로 투영
- **Purpose**: 투영된 결과를 GT(Ground Truth) 이미지와 비교하여 파라미터를 업데이트하기 위함  

$$Σ^{2D}= JW Σ^{3D}W^TJ^T$$

- **Description**: 각 3D Gaussian이 카메라 뷰를 기준으로 2D 이미지 평면에 투영됩니다. 이 투영된 이미지가 이후 Loss 계산의 기준이 됩니다.

투영 단계에서는 초기화된 3D Gaussian 분포를 카메라 뷰를 기준으로 2D 이미지 평면에 투영한다. 이 과정에서 각 Gaussian 분포가 이미지 평면에 사영되어 각 픽셀에 대응되는 2D Gaussian 형태로 나타난다. 투영된 이미지는 Loss 계산에 활용되며, 최종적인 학습 목표인 GT 이미지와 비교하여 파라미터 업데이트의 기준이 된다.

#### 1-3) Differentiable Tile Rasterizer
- **Process**: Differentiable한 Tile Rasterization을 통해 2D Gaussian들을 하나의 이미지로 생성
- **Output**: Rasterized 2D 이미지
- **Description**: Differentiable Tile Rasterizer는 투영된 Gaussian들을 하나의 2D 이미지로 합성하여 최종적으로 모델이 생성한 이미지를 출력합니다. 이 과정은 미분 가능하므로 최적화에 사용됩니다.

Differentiable Tile Rasterizer는 투영된 2D Gaussian 분포를 합성하여 단일 이미지로 만든다. 이 단계에서 각각의 2D Gaussian은 래스터화 과정에서 이미지 평면의 해당 위치에 배치되며, 최종적으로 모델이 생성한 2D 이미지가 출력됩니다. 중요한 점은 이 래스터화 과정이 미분 가능하다는 것이다. 이를 통해, 생성된 이미지와 GT 이미지 사이의 오차에 따른 Gradient를 계산하고 역전파할 수 있다.

#### 1-4) Gradient Flow
- **Process**: 생성된 이미지와 GT 이미지 사이의 Loss를 계산하고, Loss에 따른 Gradient를 전파
  
$$L = (1 - \lambda) L_1 + \lambda L_{D\text{-}SSIM}$$

- **Description**: Loss를 통해 계산된 Gradient를 역전파하여 각 파라미터가 업데이트될 수 있도록 합니다. 이는 모델이 GT 이미지에 더 가깝게 학습되도록 합니다.

모델이 생성한 이미지와 GT 이미지 사이의 Loss를 계산하고, 이 Loss로부터 구해진 Gradient를 각 파라미터로 역전파한다. 이를 통해 3D Gaussian의 위치, 크기, 밀도 등 파라미터들이 조정되며, 학습이 진행됨에 따라 모델이 생성하는 이미지가 GT 이미지와 가까워지도록 최적화된다.

#### 1-5) Adaptive Density Control
- **Process**: Gradient에 기반하여 Gaussian 형태를 변환

![adaptive](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/adaptive.png)

- **Description**: Gradient를 기반으로 각 Gaussian의 형태(위치, 크기, 밀도 등)를 조정하여 최적화합니다. 이를 통해 Gaussian이 GT 이미지와 일치하는 방향으로 업데이트됩니다.

Adaptive Density Control 단계에서는 이전 단계에서 계산된 Gradient에 따라 3D Gaussian의 형태를 적응적으로 조정한다. 각 Gaussian의 위치, 크기, 밀도 등의 파라미터가 업데이트되어, 생성된 이미지가 GT 이미지와 더욱 일치하도록 Gaussian 분포의 세부적인 조정이 이루어진다. 이 과정을 반복하여 Gaussian 분포가 GT 이미지와 최대한 가까워지도록 학습을 진행한다.

---

### Conclusion
3D Gaussian Splatting 프로세스는 SfM(COLMAP)을 통해 획득한 3D 정보를 기반으로 Gaussian 분포를 초기화하고, 이미지 평면으로 투영 및 래스터화하여 생성된 이미지와 GT 이미지 간의 Loss를 최소화하는 방식으로 최적화된다. 각 단계에서 미분 가능한 방식으로 Gradient를 전파하며, Adaptive Density Control을 통해 Gaussian 형태를 세부적으로 조정한다. 최종적으로, 본 과정을 통해 학습된 3D Gaussian 분포는 GT 이미지에 가까운 결과를 생성할 수 있도록 최적화된다.

---

### Summary
이 과정은 COLMAP으로부터 얻은 초기 3D 정보를 바탕으로 3D Gaussian을 학습하고, GT 이미지와 비교하여 최적화하는 과정입니다. 최종적으로 Loss에 따른 Gradient가 각 단계로 전파되면서 Gaussian 분포가 GT에 가깝게 조정됩니다.

---

## Gaussian Grouping

### Process
![GG](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/GG_process.png)

#### 1) 2D Image and Mask Input

- **Input**: Multiview 2D 이미지 (Ground Truth 이미지)
- **SAM**:
  - **Input**: Multiview 2D 이미지
  - **Output**: 2D 마스크 (m)

---

#### 2) Identity Consistency across Views

- **Zero-shot Tracker**: 시점 간 아이덴티티 일관성을 유지하기 위해 마스크 연관(```Mask Association```)을 수행합니다.
  - **Input**: SAM에서 생성한 2D Mask (m)와 Camera Pose
  - **Output**: 3D Object Identity Mask $$\hat{M}$$

![Asso](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/img/methodology/Association.png)

---

#### 3) 3D Gaussian Rendering and Grouping

- **Identity Encoding**: 객체의 인스턴스 ID로 작용하여 각 3D 객체를 구분하는 데 사용됩니다.

  $\text{Id Parameter} = \text{Identity Encoding\}(e_i) = SH \text{ Coefficient}$

  - SH Parameter $c_l^m$

    $c_l^m\approx {{4\Pi}\over{N}}\sum_{i=1}^N f(\theta_i,\phi_i)Y_l^m(]theta_i,\phi_i)$

1. **Projection from 3D to 2D**:
  - 3D Covariance Matrix ($\Sigma_{3D}$)을 2D로 투영하여 다음과 같이 변환합니다:  

  $$Σ^{2D}= JW Σ^{3D} W^TJ^T$$ 

2. **2D 이미지에서 픽셀별 특징 계산**:
  - 각 픽셀의 Identity feature $E_{id}$는 다음과 같이 계산됩니다:  

  $$E_{\text{id}} = \sum_{i \in \mathcal{N}} e_i \alpha'_i \prod{j=1}^{i-1} (1 - \alpha'_j)$$  
    where,  $$\alpha'_i(x) = \exp \left( - \frac{1}{2} (x - \mu_i)^T (\Sigma^{2D})^{-1} (x - \mu_i) \right)$$  

  - **참고**: $$E_{\text {id}}$$는 2D 이미지의 각 픽셀에서 계산된 Identity Feature으로, 픽셀이 어떤 객체에 속하는지를 나타냅니다.

---

#### 4) Grouping Loss

- **Input**: 2D 이미지 평면의 각 픽셀에 대한 Identity Feature $E_{id}$

1. **2D Identity Loss ($\mathcal{L}_{2D}$)**:
   - $$E_{id}$$를 MLP에 통과시키고 SoftMax 연산을 적용하여 각 픽셀이 K개의 카테고리(객체 클래스) 중 하나에 속하도록 분류합니다.

2. **3D Identity Loss ($\mathcal{L}_{3D}$)**:
   - KL Divergence를 사용하여 동일 객체에 속하는 가우시안들이 유사한 E_id 값을 가지도록 하여 아이덴티티 인코딩의 일관성을 유지합니다.

$$L_{3d} = \frac{1}{m} \sum{j=1}^{m} D_{\text{KL}}(P \parallel Q) = \frac{1}{mk} \sum_{j=1}^{m} \sum_{i=1}^{k} F(e_j) \log \left( \frac{F(e_j)}{F(e_i')} \right)$$

3. **Final Loss ($\mathcal{L}_\text{render}$)**:
   - 재구성 손실과 아이덴티티 손실을 결합하여 최종 손실을 계산합니다:  

$$L_{{render}} = L_{\text{rec}} + L_{\text{id}} = L_{\text{rec}} + \lambda_{\text{2d}} L_{\text{2d}} + \lambda_{\text{3d}} L_{\text{3d}}$$  

![loss](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/methodology/grouping.png)

---

## Gaussian Composition

### Concatenated Gaussians

#### 1) Prepare Data

- $Obj_1$ = Point Cloud $P_1$
- $Obj_2$ = Point Cloud $P_2$

---

#### 2) Apply Transformation Matrix

- Purpose : $P_1$ 또는 $P_2$ 둘 중 하나의 Point Cloud 좌표계로 다른 하나의 Point Cloud를 이전

```python
transform = torch.tensor([
    [1.000000, 0.000000, 0.000000, 0.000000],  # 회전 + 이동(x)
    [0.000000, 1.000000, 0.000000, 0.000000], # 회전 + 이동(y)
    [0.000000, 0.000000, 1.000000, 0.000000],  # 회전 + 이동(z)
    [0.000000, 0.000000, 0.000000, 1.000000]], device="cuda")
```

1. 상위 3x3 부분:
    
    회전과 스케일링을 포함\
    각 열은 각 축에 대한 변환을 나타냄
    
2. 마지막 열의 처음 3개 요소:
    
    평행 이동(translation) 벡터\
    각각 x, y, z 축으로의 이동량

3. 마지막 행 [0,0,0,1]:

    동차 좌표계를 위한 고정값


   $P_1'=P_1 T$

---

#### 3) Concatenate

```python
torch.concat(p1,p2, dim=0)
```

단순한 데이터 연결이 아니라 두 가우시안을 3D 공간에서 합성하는 것이다.
각 가우시안은 자신의 공간적 특성(위치, 크기, 방향)과 시각적 특성(색상, 불투명도)을 유지하면서 하나의 통합된 표현으로 결합된다.

---

## Summary

- **Multiview 2D Image**는 **SAM**을 통해 **2D 마스크**로 변환됩니다.
- **Zero-shot Tracker**는 이러한 마스크와 카메라 포즈를 사용하여 시점 간에 일관된 **3D Object Identity Mask** $\hat{M}$를 생성합니다.
- **3D Gaussian Rendering**을 수행하여 가우시안을 2D 공간으로 투영하고 각 픽셀의 Identity Feature (E_id)을 계산합니다.
- **Grouping Loss**를 적용하여 아이덴티티 일관성을 최적화하며, 2D 및 3D 아이덴티티 손실을 활용합니다.
- **Final Loss**는 재구성 손실과 아이덴티티 손실을 결합하여 3D 객체 그룹핑의 일관성을 보장합니다.
