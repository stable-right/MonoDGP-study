```markdown
# CHANGELOG

## 2025-08-31
- 추가: `lib/datasets/kitti/kitti_eval_python/iou_backend.py` (OpenCV CPU IoU)
- 수정: `lib/datasets/kitti/kitti_eval_python/eval.py` (IoU import 교체)
- 수정: `"lib/models/monodgp/ops/src/cuda/ms_deform_attn_cuda.cu"`
  - `.type().is_cuda()` → `.is_cuda()`
  - `AT_DISPATCH_FLOATING_TYPES(value.type(),` → `AT_DISPATCH_FLOATING_TYPES(value.scalar_type(),`
- 수정: `lib/models/monodgp/ops/modules/ms_deform_attn.py`
  - `_LinearWithBias` alias, `torch.overrides` fallback 추가
- 수정: `lib/helpers/save_helper.py`
  - `torch.serialization.add_safe_globals`로 numpy 타입 allowlist
- 문서: `docs/` 일괄 추가 (WINDOWS_PORT, IOU_BACKEND, MSDEFORMATTN, CHECKPOINT_LOADING, TRAINING_GUIDE)
- 설정 예시: `configs/monodgp_windows_example.yaml` 추가
