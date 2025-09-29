## IOU_BACKEND (OpenCV, CPU)

### 교체 이유
- 일부 최신 GPU 조합(예: RTX 50xx, SM 12.0)에서 Numba CUDA 경로가 **NVVM/컨텍스트 초기화 이슈**로 불안정할 수 있음.
- OpenCV 기반 **CPU 백엔드**는 항상 동작하며 **계산 결과(값)는 동일**(속도만 느려짐).

### 파일/연결
- 파일: `lib/datasets/kitti/kitti_eval_python/iou_backend.py`
- 사용(변경 없음):
  ```python
  # eval.py
  from .iou_backend import rotate_iou_gpu_eval

## 입력 형식
- 박스: [cx, cy, w, h, yaw], yaw는 라디안(rad), 시계방향(CW) 양수
- OpenCV는 degree + CCW → 내부에서 deg = -rad * 180/pi 변환

## criterion
- -1: Inter / Union (일반 IoU)
- 0 : Inter / GT 면적
- 1 : Inter / DT 면적
