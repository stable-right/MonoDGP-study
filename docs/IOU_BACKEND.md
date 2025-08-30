## IOU_BACKEND (OpenCV, CPU)

## 교체 이유
- 원본 Numba CUDA IoU는 최신 GPU에서 드라이버 초기화 실패/컨텍스트 이슈가 잦음.
- OpenCV CPU 백엔드는 항상 동작하고, mAP 계산은 동일(속도만 살짝 느려짐).

## 파일/연결
- 파일: `lib/datasets/kitti/kitti_eval_python/iou_backend.py`
- `eval.py`에서 import를 아래처럼 유지
  ```python
  from .iou_backend import rotate_iou_gpu_eval
```
```
## 입력 형식
- 박스: [cx, cy, w, h, yaw], yaw는 라디안(rad), 시계방향(CW) 양수
- OpenCV는 degree + CCW → 내부에서 deg = -rad * 180/pi 변환

## criterion
- -1: Inter / Union (일반 IoU)
- 0 : Inter / GT 면적
- 1 : Inter / DT 면적
