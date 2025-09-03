# MonoDGP-study (Windows + CUDA 12.8, RTX 50xx)

본 레포는 [PuFanqi23/MonoDGP](https://github.com/PuFanqi23/MonoDGP)를 Windows + CUDA 12.8 + RTX 50xx(SM 12.0) 환경에서  실행/학습/평가 가능 하도록 변경 후 공부/연구

원본: https://github.com/PuFanqi23/MonoDGP
 

---

## 환경 요약

- OS: Windows 10/11 (64-bit)
- GPU: NVIDIA  RTX 5060 Ti (SM 12.0) 
- CUDA Toolkit:  12.8 
- Visual Studio:  2022 (MSVC 19.x) 
- Python:  3.9  (conda env: `monodgp50`)
- PyTorch:  2.8.0+cu128 
- TorchVision:  0.23.0+cu128 
- 기타: `opencv-python==4.6.0.66` (IoU용), `ninja`, `setuptools`, `wheel`

> 전체 패키지 버전은 [`requirements.txt`](./requirements.txt) 참고.

---

## 논문 요약

문제의식
라이다 없이 카메라 하나(단안 영상)만으로 3D 공간에서 차량 같은 물체의 위치, 크기, 방향을 정확히 예측할 수 있을까?

핵심 아이디어

이미지에서 깊이 단서를 뽑아내고, 카메라 기하(Geometry) 정보를 이용해 이미지를 BEV(Bird’s-Eye View, 위에서 본 평면) 로 변환한다.

이렇게 하면 원근 왜곡이 줄고, 물체의 실제 크기와 방향이 더 잘 드러나므로 3D 박스 예측이 안정된다.

흐름

입력: 단일 RGB 이미지

깊이 인지(Depth-aware): 픽셀별 거리 단서를 추정해 특징에 반영

기하 인지(Geometry-aware): 카메라 파라미터를 활용해 이미지를 BEV 좌표로 정렬

BEV Head: BEV 위에서 중심, 크기, 높이, 방향(yaw)을 예측

출력: 3D 박스 (2D/BEV/3D 결과가 일관되도록 학습)

왜 이렇게 하나?

이미지 공간은 원근 때문에 멀리 있는 물체가 작게 보인다.

BEV로 바꾸면 실제 크기 기준으로 표현되므로 예측이 쉬워진다.

깊이 단서와 기하 정렬을 합치면 단안 탐지의 가장 큰 약점(깊이 불확실성)을 줄일 수 있다.

---

한 줄 요약
“이미지에서 깊이와 기하 정보를 추출해 BEV로 정렬하고, 그 위에서 3D 박스를 예측하는 방식”

## 핵심 변경 (요약)

1)  MSDeformAttn CUDA 확장 빌드(Windows, SM 12.0)   
   - `value.type()` → `value.scalar_type()` 등  PyTorch 2.x API  호환화  
   - Python 모듈에서 `torch.overrides` / `torch._overrides`  분기 임포트   
   - 빌드 시 `TORCH_CUDA_ARCH_LIST=12.0` 지정 (RTX 50xx 지원)

2)  BEV IoU: OpenCV(CPU) 백엔드   
   - 원본 `numba.cuda` 기반 IoU가 Windows/드라이버 충돌 →  CPU OpenCV `intersectConvexConvex`로 대체   
   - 정확도 동일, 속도만 느려짐(평가 시간 증가)  
   - `eval.py`의 `rotate_iou_gpu_eval` import를 `iou_backend.py`로  교체 

3)  체크포인트 로딩(PyTorch 2.6+)   
   - 기본 `weights_only=True`로 바뀌면서 생기는 Unpickling 에러 대응  
   - `save_helper.py`에서  안전 전역 허용 + `weights_only=False` 로 로드

자세한 내용은 `docs/` 문서 참조:
- [WINDOWS_PORT.md](./docs/WINDOWS_PORT.md), [MSDEFORMATTN.md](./docs/MSDEFORMATTN.md), [IOU_BACKEND.md](./docs/IOU_BACKEND.md), [CHECKPOINT_LOADING.md](./docs/CHECKPOINT_LOADING.md)

---

## 데이터 경로 (KITTI)

- 로컬: `..\MonoDGP\data\kitti`  
- `configs/monodgp_windows_example.yaml`에서:
  ```yaml
  dataset:
      root_dir: C:\Users\PUBLIC\kitti   # 예시(문서에서 바꾸라고 안내)

  ```

  ## 평가/학습

  ```
  python tools/train_val.py --config configs\monodgp_windows_example.yaml
  python tools/train_val.py --config configs\monodgp_windows_example.yaml -e
  ```
