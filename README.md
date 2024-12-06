# 🎓Capstone-SW-Project
2024 졸업 프로젝트 - 3D Gaussian Splatting을 이용한 3D Synthesized Space Reconstruction

Professor : 이성윤 교수님\
Co-worker : 박현준, 임도현

---

## Table of Contents
1. Objective 
2. Environment and Implementation
3. Methodology
4. Results
5. Analysis
6. Conclusion
7. References

---

## 1. Objective
최신 Computer Vision 기술인 3D Gaussian Splatting을 이용하여 서로 다른 배경에 존재하고 있는 Object들을 3DGS로 렌더링한 뒤 이들의 Point Cloud들을 합성해서 3D Space에 Reconstruct 하는 프로젝트입니다.

한 가지 예시로, Gaussian Grouping에서 제공하는 lerf-mask dataset으로 3DGS를 학습시킨 뒤 렌더링한 결과를 viewer를 통해 확인해보면 다음과 같은 결과를 확인할 수 있습니다.

![3DGS](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/rendering/3DGS.gif)

이번 프로젝트에서는 기존에 존재하는 dataset들이 아닌, 저희가 직접 촬영한 동영상을 특정 frame 단위로 잘라 이미지로 변환하여 custom dataset을 만든 뒤, 이를 학습시켜서 렌더링한 결과를 이용하여 객체를 합성하는 task를 진행하려고 합니다.

---

## 2. Environment and Implementation
- Environment Setting : [EnvSetting.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/Env_Setting.md)
- Implementation detail : [Implement.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/Implement.md)

---

## 3. Methodology
- Methodology : [Methodology.md](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/Methodology.md)

---


## 4.Results

### COLMAP

#### # 1바퀴 촬영
|한양대학교|혼천의|세종대왕|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/COLMAP/hyu.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/COLMAP/clk.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/COLMAP/king.jpg)|

#### # 2바퀴 이상 촬영
|측우기|혼천의|사람|
|:--:|:--:|:--:|
|![4](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/COLMAP/rain.jpg)|![5](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/COLMAP/hon.jpg)|![6](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/COLMAP/dororo.jpg)|


### Point Cloud

|Wide-view|Front|Rear|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/pointcloud1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/pointcloud2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/pointcloud3.jpg)|

## Rendering

### Images

|한양대|+|혼천의|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/clock1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/clock2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/clock4.jpg)|
|한양대|+ 혼천의|+ 세종대왕|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/result1.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/result2.jpg)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/result3.jpg)|

### GIF

|원본|결과물(세종대왕)|결과물(측우기)|
|:--:|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/rendering/concat.gif)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/rendering/synth_result.gif)|![3](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/rendering/hyuhonrain.gif)|

---

## 5.Analysis

<Gaussian Grouping>

[장점]
1. Image 약 150~200 장으로 3D Space를 복원할 수 있다.
2. Gaussian Grouping의 경우 SAM (Segment Anything)을 이용하여 mask에 index 값을 부여한 뒤, 그 index 값을 이용하여 원하는 객체에 속하는 Gaussian들을 Clustering 하는 과정을 통해 index 값을 갖는 객체를 제외한 나머지 부분을 제거할 수 있다.
3. Point Cloud를 합성하는 과정을 통해 서로 다른 Space를 하나의 Space로 가져올 수 있다.
4. Style transfer를 통해 특정 객체를 원하는 모습으로 변환할 수 있다.

[단점]
1. 촬영하고자 하는 대상의 크기가 너무 커서 객체의 위쪽을 촬영하지 못할 경우, Rendering 했을 때 Quality가 떨어진다.
2. Camera의 position에 영향을 많이 받기 때문에 Occlusion이나 Unseen view에 대해서는 GT와 많은 차이가 존재한다.
3. Index 값을 올바르게 넣지 않을 경우 원하지 않는 부분이 Grouping 되거나, Masking 영역이 제대로 제거 되지 않아 수 많은 artifact들이 생기게 된다

|Artifact 예시|정확한 객체 분리 예시|
|:--:|:--:|
|<img src="https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/same_index.jpg" width="800">|<img src="https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/rendering/remove_bg.png" width="600">|

---

### 단점 해결 방안
1. Custom dataset을 수집할 때 최소 2바퀴 이상 촬영을 한다. 그래야 더욱 정확하게 객체에서 feature를 뽑아낼 수 있다.
2. Config 파일에 들어가는 적절한 hyper parameter 값 (threshold, index) 을 찾는다.
3. 촬영을 할 때, 측우기 COLMAP 처럼 하부/중부/상부로 나눠서 촬영을 하면 더욱 정확한 3차원 복원이 가능하다.
4. 빛의 영향을 많이 받는 경우 Camera pose estimation의 정확도가 떨어지기 때문에 가급적 광원이 고정되어 있고, 균일하게 빛을 받는 상태에서 dataset을 수집한다.
5. 크기가 큰 물체의 경우 드론을 이용하거나 최대한 전체적인 모습이 담길 수 있도록 촬영을 한다.
6. 정확한 index 값을 config 파일에 넣는다 $\rightarrow$ **[find_idx.py](https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/find_idx.py)로 직관적인 index 값 확인 가능**
7. Pointcloud 파일에서 outlier들을 제거해서 artifact가 생기는 것을 최대한 방지한다.

   >기존의 배경을 지운 pointcloud 파일을 cloudcompare로 확인을 해보면 객체 위에 존재하는 point들의 밀도가 상당히 높은 것을 확인할 수 있다. 하지만, 아래의 사진을 보면 객체 주변, 심지어는 객체와 멀리 떨어진 곳에도 불필요한 point들이 여럿 존재하는 것을 알 수 있다. 이 point들이 나중에 artifact의 원인이 될 수 있기 때문에 후처리로 완전히 제거되지 않은 point들을 지워주는 것이 보다 깔끔한 rendering이 될 것이다.
   >
   >**실행 방법**
   >```bash
   > python remove_artifact.py -d <dataset name>
   >```
   
   <p align="center">
     <img src="https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/docs/img/explain/before.png" alt="before" width="700">
   </p>

   |KDTree Algorithm|DBSCAN Algorithm|
   |:--:|:--:|
   |<img src="https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/docs/img/explain/kdtree.png" width="2000"> | <img src="https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/docs/img/explain/dbscan.png" width="400"> |
   |이 방식의 경우 배경은 깨끗하게 지워지지만 객체에 해당하는 point들의 일부도 같이 지워진다는 문제점이 있었다.|DBSCAN (Density-Based Spatial Clustering) 방식을 사용하게 되면 밀도를 기준으로 clustering을 하기 때문에 배경을 제거한 point cloud 파일에 적용을 하게 되면 point의 밀도가 높은 객체 주변에 존재하는 point들이 살아남게 된다. KDTree algorithm을 사용했을때 보다 객체 위치에 존재하는 point들이 많이 보전된 것을 확인할 수 있다.|

   |HDBSCAN|Mean Distance Threshold|
   |:--:|:--:|
   |<img src="https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/docs/img/explain/hdbscan.png" width="2500">|<img src="https://github.com/Capstone-SW-Project/3D-Synthesized-Space-Reconstruction-using-3DGS/blob/main/docs/img/explain/meandist.png" width="2000">|
   |HDBSCAN (Hierarchical DBSCAN)의 경우 point들이 고르게 분포해 있는 것이 아니라 특정 위치에 뭉쳐있는 모습을 확인할 수 있다. 그로 인해 quality가 떨어진다.|이 방식의 경우 서로 다른 point들 간의 거리를 구한 뒤 평균값을 구해서 이 값을 threshold로 설정한 뒤 threshold를 넘은 거리에 위치한 point를 버리는 방식이다. 이 방식도 좋은 성능을 보이지만, point들의 개수가 많아지면 그에 비례하게 연산량도 많아지기 때문에 DBSCAN algorithm이 가장 최적의 방식이라는 결론에 도달했다.|

### Ablation study
#### # 2바퀴 이상 촬영을 한 뒤 렌더링한 측우기의 모습

|좌|우|
|:--:|:--:|
|![1](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/result5.jpg)|![2](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/result/result4.jpg)|

3바퀴를 돌며 하부/중부/상부를 촬영한 측우기의 경우 받침석에 각인되어 있는 한자까지 상당히 고퀄리티로 복원이 된 것을 확인할 수 있다.

---

## 6.Conclusion

이번 프로젝트를 통해 컴퓨터 비전 분야의 최신 연구 주제에 대해 깊이 있는 이해를 얻었습니다. 특히, **Colmap**, **3D Gaussian Splatting**, **Feature 3DGS**, **Segment Anything**, **Gaussian Grouping**과 같은 논문을 통해 관련 개념을 습득하고, 해당 영역에서의 최신 연구 동향을 경험했습니다.

논문 학습에 그치지 않고, 실제 구현 코드를 바탕으로 이론을 실습하고 동작 원리를 파악하는 과정을 거치면서 프로젝트의 목표를 명확히 설정했습니다. 이후, 커스텀 데이터를 생성하여 이를 학습에 활용하고 목표를 달성하고자 노력하였습니다. 비록 처음 의도한 목표를 완벽하게 달성하지는 못했지만, 원인을 분석하며 이 문제를 해결하기 위한 방안을 모색하는 과정을 통해 연구자 주도의 문제 해결 방식을 체득할 수 있었습니다.

이번 프로젝트는 컴퓨터 비전 연구에서의 실질적 역량을 강화하는 계기가 되었으며, 앞으로도 이러한 과제를 극복하며 관련 기술을 발전시킬 동력이 될 것입니다.

---

## 7.References
1. Schonberger, Johannes L., and Jan-Michael Frahm. "Structure-from-motion revisited." Proceedings of the IEEE conference on computer vision and pattern recognition. 2016.
2. Kerbl, Bernhard, et al. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." ACM Trans. Graph. 42.4 (2023): 139-1.
3. Ye, Mingqiao, et al. "Gaussian Grouping: Segment and Edit Anything in 3D Scenes." arXiv preprint arXiv:2312.00732 (2023).
4. Shijie Zhou, et al. "Feature 3DGS: Supercharging 3D Gaussian Splatting to Enable Distilled Feature Fields." Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024, pp. 21676-21685
5. Alexander Kirillov, et al. "Segment Anything." Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2023, pp. 4015-4026
