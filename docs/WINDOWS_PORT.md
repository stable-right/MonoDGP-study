# WINDOWS_PORT

## 목표
- RTX 50xx(SM 12.0) + CUDA 12.8 + Torch 2.8.0(+cu128) 조합에서   안정 실행  .

## 핵심 포인트
- `nvcc`가   CUDA 12.8  을 가리키게 환경 변수 설정
- Visual Studio 2022(Build Tools) 설치 (CUDA 컴파일 연동)
- `TORCH_CUDA_ARCH_LIST=12.0` 설정(아키텍처 지정)

## 빌드 명령(ops 디렉토리에서)
```bat
cd lib\models\monodgp\ops
set TORCH_CUDA_ARCH_LIST=12.0
set CUDA_HOME=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8
python setup.py clean
python setup.py build_ext --inplace
