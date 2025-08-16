# 설정 변경 내역

### 사용 환경
- OS: Windows 11 (Anaconda 환경)
- Python 3.9 / CUDA 11.1
- GPU: RTX 5060ti 16GB

### 수정한 설정 (configs/monodgp.yaml 기준)
- `batch_size`: 8 → 4  (VRAM 부족 문제)
- `input_shape`: [1280, 384] → [960, 288] (모델 경량화)
- `num_workers`: 4 → 2  (Windows 환경 호환성)
- `epochs`: 50 → 100  (성능 수렴 확인 목적)
- `lr`: 2.5e-4 → 1.0e-4  (작은 배치 대응)
