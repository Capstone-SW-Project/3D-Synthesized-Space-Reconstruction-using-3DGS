# Implementation

이 파일에서는 여러 장의 input image들로 부터 3D space를 복원하고, 복원한 space에 서로 다른 배경에 존재하고 있던 객체들을 합성하는 task의 전체적인 실행 방법에 대한 설명하도록 하겠습니다.

## COLMAP

![colmap_impl](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/colmap_impl.png)
COLMAP 실행 후 노란색 형광펜으로 칠한 부분 (Automatic Reconstruction)을 클릭하면 위와 같은 화면이 나옵니다.

그 뒤, ```Workspace folder```에는 COLMAP을 돌린 뒤 결과물이 저장될 폴더의 경로를 입력하고, ```Image folder```에는 COLMAP에 넣을 input image들이 들어 있는 폴더의 경로를 입력합니다.

이 때, input image의 경우 크기가 너무 크면 COLMAP이 돌아가는데 상당히 많은 시간이 소요되기 때문에 시간 단축을 위해 image의 크기를 1000x1000 이하로 줄이는 것을 추천드립니다. Image 크기를 줄이는 방법은 같이 있는 ```image_resize.py``` 파일에 imagepath와 savepath를 입력해서 실행을 하면 됩니다.

```python
python image_resize.py
```

아래 옵션에서는 ```Dense model```은 필요 없기 때문에 체크 해제를 하고 ```Sparse model```만 생성을 하도록 설정한 뒤 GPU 여부를 체크한 뒤 ```Run```을 클릭하면 작동이 됩니다.

다 끝나면 아까 지정했던 ```Workspace folder```에 결과물들이 저장 됩니다.

![colmap_output](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/colmap_output.png)

> 한가지 더 중요한 내용은, 3DGS를 돌릴 때 ```SIMPLE PINHOLE``` 또는 ```PINHOLE``` 카메라로 세팅을 해주어야하는데, 이 과정은 다음과 같습니다.
> 
>1. File - New project - [database, images] 입력
>2. Processing - Feature Extraction에서 ```SIMPLE PINHOLE``` 옵션을 선택하고 Extract를 클릭합니다. 제대로 바꼈는지 확인하고 싶다면 Processing - database management에 들어가서 카메라 옵션이 ```SIMPLE PINHOLE```로 바꼈는지 확인하면 됩니다.
> 
> ![pinhole](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/pinhole.png)
>
>3. Auto reconstruction을 클릭한 뒤 ```database``` 파일 경로와 ```images``` 폴더 경로를 입력합니다.

여기까지 하게 되면 ```cameras.json```, ```cfg_args``` 파일들과 sparse 폴더 내에 ```cameras.bin```, ```images.bin```, ```points3D.bin``` 파일들이 생성 됩니다.
이제 이 결과물들을 Gaussian Grouping을 세팅해 놓은 폴더에 복사를 해서 input으로 입력을 해주면 됩니다.

## Gaussian Grouping

Gaussian Grouping의 경우 논문의 저자가 Github에 적어 놓은 설명 그대로 진행을 하면 됩니다.

[출처 : Gaussian-Grouping (train.md)](https://github.com/lkeab/gaussian-grouping/blob/main/docs/train.md)

```

먼저 input 폴더를 생성한 뒤, 아래와 같이 input image의 경로를 설정합니다.

<location>
|---input
    |---<image 0>
    |---<image 1>
    |---...
```

SAM object mask로 전환을 합니다.

```
bash script/prepare_pseudo_label.sh [폴더 이름] 1
```

전환을 하는 이유는 원하는 객체만을 가져오기 위해서는 segmentation을 통해 원하는 객체를 제외한 나머지 배경 부분을 masking한 뒤, ```edit_object_removal.py``` 파일을 실행해서 원하는 객체 부분을 가져올 수 있기 때문입니다.

### Segmentation

Segmentation을 해서 객체를 지정한 뒤 그 객체 또는 배경을 지워야 하는데, 위에서 ```prepare_pseudo_label.sh``` 파일로 segmentation 된 image들이 생성되었다면, 이 image들에서 원하는 객체에 대한 정보를 불러와야 합니다. 그러기 위해서 ```Output/Annotations``` 폴더에 들어가 보면 어두운 색깔들로 segmentation이 된 image들이 여러장 존재하는 것을 확인할 수 있습니다. 여러 장의 Annotated image들 중 임의로 하나를 다운로드 받아서 그림판으로 연 뒤, 스포이드 모양으로 원하는 위치를 찍어서 색깔 정보를 보게 되면 아래의 그림처럼 RGB 값이 모두 동일한 정수값으로 주어져 있는 것을 확인할 수 있습니다.

![index](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/index.png)

이 값이 곧 segmentation을 했을 때 객체가 갖고 있는 index가 됩니다. 즉, 아래의 그림 처럼 Gaussian 들이 grouping을 한 후에 갖는 index 값을 의미합니다. 이 때 하나의 이미지에서 객체가 갖고 있는 index 값은 여러 개 일 수도 있기 때문에 모든 index 값을 찾아서 입력으로 넣어주어야 합니다.

![GG](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/Gaussian_Grouping.jpg)

Index 값들을 모두 찾았다면 그 값들을 Gaussian Grouping - config 폴더에 ```[폴더명].json``` 파일을 생성한 뒤 다음과 같이 코드를 적고 index numbers 배열에 index 값들을 모두 넣어준 뒤 파일을 저장하면 됩니다.

```json
{
    "num_classes": 256,
    "removal_thresh": 0.9,
    "select_obj_id" : [index numbers]
}
```

마지막으로 아래의 파일을 실행시키면, 해당 index 부분을 제외한 나머지 부분들을 지워주게 됩니다.

```bash
bash script/edit_object_removal.sh output/bear config/object_removal/[json파일 이름].json
```

|Before|After|
|:--:|:--:|
|![before](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/before.jpg)|![after](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/after.jpg)|


### Training

모든 준비가 되었다면, training을 통해 point cloud를 생성하고 image들로 feature들을 뽑아서 rendering을 해야 합니다.

```
bash script/train.sh [폴더 이름] 1
```

Segmentation과 Training까지 끝나게 되면 output 폴더 아래에 다음과 같이 폴더가 구성됩니다.

```
|---output
    |---[폴더명]
        |---Annotations
        |---Annotations_color
        |---point_cloud
            |---iterations_5000
            |---iterations_7000
            |---iterations_30000
        |---test
        |---train
            |---ours_[#iteration]
                |---concat
                |---gt
                |---gt_objects_color
                |---object_features16
                |---objects_pred
                |---renders
        |---Visualizations
```

생성된 image들의 결과를 확인하기 위해 나머지 다섯 개의 image를 하나로 합쳐 놓은 concat image를 보면 ```gt - renders - gt_objects_color - objects_pred - object_features16``` 순서로 image가 생성되어 있어서 output들을 한 번에 확인할 수 있습니다.

![concat](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/concat.jpg)

이 과정이 끝났다면 둘 중 하나의 과정으로 넘어가면 됩니다.

1. 객체나 배경을 지우고 싶다면 object_removal 과정을 진행
2. rendering된 image를 3D space에 복원한 결과를 보고 싶다면 viewer를 이용하여 확인

## CloudCompare

[CloudCompare](https://www.danielgm.net/cc/)를 설치한 뒤 실행하고 원하는 2개의 point cloud (ply) 파일 [배경 / 객체]들을 가져옵니다.
정상적으로 loading이 되었다면 point cloud를 조작해서 배경에서 원하는 위치로 객체를 위치시킵니다.

한 가지 예시로, 한양대 본관 앞 사자상 위치에 광화문에 있는 세종대왕 동상을 갖다 놓고 싶다면, 한양대를 배경으로 하는 point cloud 파일을 로드한 뒤, 세종대왕 동상의 배경을 제거한 point cloud 파일을 가져와서 위치를 조정하면 됩니다.

>아래의 그림에서 노란색/초록색으로 표현된 point들이 한양대, 빨간색으로 표현된 point들이 세종대왕 동상에 대한 point cloud 입니다.

![synthesize](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/cloudcpr.png)

그 다음으로 point cloud를 조작한 객체의 정보를 클릭한 뒤, property 창에서 제일 아래로 내려가면 어떤 행렬이 생성되게 됩니다.

![matrix](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/image.png)

4x4 행렬이고, 1행1열부터 3행3열까지는 rotation, 4열은 translation에 대한 정보를 갖고 있습니다. 즉, 해당 객체를 초기 위치에서 얼마만큼 움직였는지에 대한 정보를 나타냅니다.

이 행렬을 복사해서 ```composition_ply.py``` 파일의 transform에 값을 넣고 ply 파일 위치와 savepath를 지정해준 뒤 파일을 실행하면 됩니다. 이 때, 주의할 점은 point cloud 파일을 병합하는 과정이기 때문에 local이 아닌 anaconda env에서 실행을 해야합니다.

```python
# 객체
xyz1, features_dc1, features_rest1, opacity1, scaling1, rotation1= load_ply("path to object ply")
# 배경
xyz2, features_dc2, features_rest2, opacity2, scaling2, rotation2= load_ply("path to background ply")

...

savepath = '새롭게 생성한 ply 파일이 저장될 위치'

scaling_inverse_activation = torch.log
# 이 부분에 CloudCompare에서 얻은 matrix value를 넣으면 됨
transform = torch.tensor(
    [[-0.561683, 0.188307, 0.805638, -1.117590],
     [-0.101479, 0.950722, -0.292968, -0.038309],
     [-0.821106, -0.246310, -0.514895, 1.115122],
     [0.000000, 0.000000, 0.000000, 1.000000]], device="cuda")
save_transform = transform.cpu().numpy()
```
여기까지 한 뒤 실행을 하면 됩니다. 다만, ```composition_ply.py``` 파일은 GPU를 사용하기 때문에 Gaussian Grouping과 같은 디렉토리에 위치시켜서 Gaussian Grouping을 실행할 때 사용한 conda 가상환경으로 실행을 하거나, GPU가 있는 PC라면 conda 가상환경을 이용하여 실행을 하면 됩니다.

```bash
# Gaussian Grouping 가상환경 설정과 동일
conda create -n GG python=3.8 -y
conda activate GG 

conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
pip install plyfile==0.8.1
pip install tqdm scipy wandb opencv-python scikit-learn lpips

# 파일 실행
cd <dir_path>
python composition_ply.py
```

새롭게 만들어진 point cloud 파일을 복사한 뒤, 배경 또는 객체의 ```cameras.json```, ```cfg_args``` 파일과 같은 폴더에 point_cloud 폴더를 생성하여 그 안에 붙여넣기를 한 뒤 동일한 방식으로 viewer를 통해 결과를 확인하면 됩니다.

예시로, 한양대 사자상 앞에 광화문 세종대왕 동상 앞에 있는 혼천의 동상을 가져다 놓으면 아래와 같이 rendering이 됩니다.

![final](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/img/explain/final.png)
