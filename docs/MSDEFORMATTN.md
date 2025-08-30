# MSDEFORMATTN (CUDA 확장, Torch 2.x 호환)

## 문제
- 예전 코드가 `value.type()`(Type 객체) 기반 매크로 호출 → Torch 2.x에서 호환성 문제.

## 해결 개념
- **스칼라 dtype**만 필요하므로 `value.scalar_type()`로 대체.
- CUDA 텐서 체크도 `.type().is_cuda()` 대신 `.is_cuda()` 사용이 안전.

## 역할 설명(쉽게)
- 이 모듈은 **Deformable Attention**의 핵심 연산을 CUDA 커널로 실행.
- PyTorch의 dtype(float/half 등)에 맞춰 **템플릿 분기**(AT_DISPATCH)로 커널 호출.

## 빌드
- `docs/WINDOWS_PORT.md` 참고
