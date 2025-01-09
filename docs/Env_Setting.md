# Environment Setting

Gaussian Grouping을 이용하여 다른 배경에 존재하고 있던 object를 원하는 배경으로 가져와서 3D로 reconstruction을 하기 위해서는 4가지 설정이 필요합니다.

#### 1. COLMAP 설치
 
 : COLMAP을 통해 input image들을 이용하여 point cloud와 camera 정보를 얻어와야 gaussian splatting을 통해 reconstruction을 할 수 있습니다.

#### 2. Gaussian Grouping
 
 : Gaussain Grouping을 돌리기 위한 환경 설정이 필요합니다.

#### 3. CloudCompare
 
 : CloudCompare 프로그램을 설치해서 object를 옮길 배경, 옮기고 싶은 object에 대해 각각 돌린 3DGS point cloud를 불러와서 object를 배경 위에 합성합니다.

#### 4. GS Viewer
 
 : 3DGS를 돌리고 나온 output을 이용하여 제대로 rendering이 되었는지 결과물을 확인하기 위해 전용 viewer가 필요합니다.

## COLMAP

COLMAP의 경우 [Github](https://github.com/colmap/colmap/releases)에 들어가서 중간쯤에 Assets 부분에 있는 zip 파일을 cuda 유/무에 따라 설치를 하면 됩니다.

![down_colmap](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/explain/down_colmap.png)

설치를 하고 압축을 해제 하면 아래 image 같이 구성이 되어 있는 것을 확인할 수 있는데, 여기서 ```COLMAP``` 파일을 실행하면 COLMAP이 실행됩니다.

![colmap](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/explain/colmap.png)

### 실행 화면

<img src="https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/explain/colmap_exe.png" width="600">

## Gaussian Grouping

### Environment

- torch : 1.12.1
- anaconda
- GPU : GeForce RTX 3090 1대
- CUDA : 12.4

### Installation

Gaussian Grouping을 clone 해옵니다.

```
git clone https://github.com/lkeab/gaussian-grouping.git
cd gaussian-grouping
```

Anaconda 가상환경을 만들고 필수 설치파일들을 설치해줍니다.

```bash
conda create -n gaussian_grouping python=3.8 -y
conda activate gaussian_grouping 

conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
pip install plyfile==0.8.1
pip install tqdm scipy wandb opencv-python scikit-learn lpips

pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn
```

Option이긴 한데 own dataset에 mask를 얻고 싶다면 DEVA 환경도 구축하면 된다고 합니다.
```bash
cd Tracking-Anything-with-DEVA
pip install -e .
bash scripts/download_models.sh     # Download the pretrained models

git clone https://github.com/hkchengrex/Grounded-Segment-Anything.git
cd Grounded-Segment-Anything
export AM_I_DOCKER=False
export BUILD_WITH_CUDA=True
python -m pip install -e segment_anything
python -m pip install -e GroundingDINO

cd ../..
```

## Gaussian Splatting Viewer

Gaussian Splatting을 돌린 뒤 결과물을 육안으로 확인하기 위해서는 전용 viewer가 필요합니다. Linux 환경에서 설치를 해도 되지만, window에 설치하는 것을 추천드립니다.

[GS-Viewer : install](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/binaries/viewers.zip)

install을 클릭하면 zip 파일이 설치가 됩니다. 그 뒤 원하는 위치에 압축 해제를 하면 됩니다.

![viewer](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/explain/viewer.png)

압축 해제를 하게 되면 위의 그림과 같이 나오게 되고, bin 폴더에 들어가면 여러 파일들이 존재합니다. 이렇게 되면 viewer 실행 준비는 모두 끝나게 됩니다.

이제 다음으로 anaconda prompt를 켠 뒤, ```viewers\bin``` 위치로 이동해서 아래의 명령어를 입력해서 실행을 하면 됩니다.

```shell
cd [installed dir]/viewers/bin
SIBR_gaussianViewer_app -m <output 경로>
```

위의 코드를 실행하게 되면 output을 viewer로 불러와서 viewer에 결과물이 보이게 됩니다. 이 때 output 경로의 경우 예시로 다음과 같은 형태로 존재해야 합니다.

```
<location>
|---output
|   |---apple
|   |---banana
|   |---cherry
|   |---...
```

그래서 만약 3DGS를 돌린 사과를 불러오고 싶다면 output 경로에 apple 폴더까지의 경로를 입력하면 됩니다.

![output_dir](https://github.com/Capstone-SW-Project/3D-Gaussian/blob/main/docs/img/explain/output_dir.png)

3DGS output 폴더 내부를 보면 위의 그림과 같이 되어 있는데, 여기서 viewer를 통해 보기 위해서 **반드시** 필요한 파일의 경우 ```point_cloud```, ```cameras.json```, ```cfg_args``` 파일입니다. 이 파일들이 없으면 viewer로 볼 수가 없습니다.

따라서 output 폴더의 경우 다음과 같이 구성이 되어 있어야 합니다.

```
|---<output>
|   |---point_cloud
|       |---point_cloud.ply
|   |---cameras.json
|   |---cfg_args
```
