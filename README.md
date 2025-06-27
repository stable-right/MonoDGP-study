# MonoDGP-study

이 저장소는 MonoDGP(Monocular Gemetry-aware Depth-aware 3D Objec;t Detection) 기반 연구 프로젝트를 위한 코드, 데이터 구성, 실험 기록을 포함하고 있다.

# 프로젝트 개요

- 연구 주제: 단안 카메라 기반 3D 객체 검출
- 모델: MonoDGP[논문][https://arxiv.org/abs/2303.16878](https://arxiv.org/abs/2410.19590)
- 원본 코드: [https://github.com/PuFanqi23/MonoDGP](https://github.com/PuFanqi23/MonoDGP)
- 연구 목적: 논문 기반 재현 및 성능 개선, 파라미터 실험

# 연구 진행 현황

- [x] Python 3.9 + CUDA 11.1 환경 설정
- [x] C++/CUDA 커스텀 연산 빌드
- [x] KITTI 데이터셋 구성 (train/val 분할 포함)
- [x] 학습 스크립트 실행 테스트
- [ ] 파라미터 실험 및 성능 개선 진행 중
- [ ] 성능 평가 및 개선 실험 진행 중

# 환경 설정

- Python 3.9 (Anaconda 가상환경 `monodgp`)
- CUDA Toolkit 11.1
- PyTorch 1.9.0 + torchvision 0.10.0

필수 라이브러리는 `requirements.txt` 참조.

  # 주요 디렉토리 구조
  
```plaintext
MonoDGP-study/
├── configs/            # 실험에 사용한 YAML 설정 파일들
├── data/kitti/         # KITTI 데이터셋 구성 디렉토리
│   ├── ImageSets/         # train.txt, val.txt 등 split 파일
│   ├── training/          # 학습 이미지 및 라벨
│   └── testing/           # 테스트 이미지
├── docs/              # 문서 정리용 디렉토리 (설정, 결과, 로그 등)
│   ├── config_notes.md      # 설정 파일 수정 내역
│   ├── train_results.md     # 실험 결과 기록
│   └── debug_log.md         # 오류 해결 과정 정리
├── lib/               # MonoDGP 모델 및 커스텀 CUDA 연산
├── logs/              # 학습 로그 저장
├── tools/             # train/test 실행 스크립트 모음
├── split_kitti.py     # KITTI 데이터셋 train/val 분할 스크립트
├── train.sh           # 학습 실행용 bash 스크립트
└── README.md          # 프로젝트 소개 및 개요
```

# 학습 실행 방법

bash
PYTHONPATH=. python tools/train_val.py --config configs/monodgp.yaml 또는 로그 저장용 bash train.sh configs/monodgp.yaml > logs/monodgp.log

# 주요 문제 및 해결 방법

- ModuleNotFoundError: MultiScaleDeformableAttention
  원인: CUDA 확장 모듈 미설치
  해결 방법: setup.py build install 실행

- FileNotFoundError: train.txt 없음
  원인: train/val 리스트 미존재
  해결 방법: split_kitti.py 만들어 생성

- GPU부족 또는 충돌
  원인: VRAM 부족 또는 버전 호환성
  해결 방법: 작은 모델 구성, Colab에서 테스트
  
