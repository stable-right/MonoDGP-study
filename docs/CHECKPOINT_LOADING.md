# CHECKPOINT_LOADING (PyTorch 2.8)

## 배경
- PyTorch 2.6+부터 `torch.load` 기본이 `weights_only=True`.
- 예전 체크포인트에 `numpy.scalar`, `numpy.dtype` 등이 들어있으면
  → “허용되지 않은 global” 에러.

## 이 레포의 처리
- 신뢰하는 ckpt라는 전제에서 허용 목록에 numpy 타입 추가:
  - `lib/helpers/save_helper.py` 상단:
    ```python
    import numpy as np
    from torch.serialization import add_safe_globals
    add_safe_globals([np.core.multiarray.scalar])
    add_safe_globals([np.dtype])
    ```
- 이렇게 하면 `torch.load()`가 안전 모드에서도 해당 타입 허용.

