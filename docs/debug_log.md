# 디버깅 및 문제 해결 기록

## ❗ MultiScaleDeformableAttention 모듈 오류
- 에러: ModuleNotFoundError
- 조치: `lib/models/monodgp/ops` 디렉토리에서 `python setup.py build install`

## ❗ train.txt 누락 문제
- 원인: KITTI split 파일 누락
- 조치: `split_kitti.py` 실행 후 생성됨

## ❗ VRAM 부족 오류
- 현상: CUDA out of memory
- 조치: 배치, 해상도 축소 / num_workers 최소화
