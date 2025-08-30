import os
import torch
import torch.nn as nn
import numpy as np
from torch.serialization import add_safe_globals

# 필요한 numpy 타입 전부 허용
add_safe_globals([np.core.multiarray.scalar])
add_safe_globals([np.dtype])


def model_state_to_cpu(model_state):
    model_state_cpu = type(model_state)()  # ordered dict
    for key, val in model_state.items():
        model_state_cpu[key] = val.cpu()
    return model_state_cpu


def get_checkpoint_state(model=None, optimizer=None, epoch=None, best_result=None, best_epoch=None):
    optim_state = optimizer.state_dict() if optimizer is not None else None
    if model is not None:
        if isinstance(model, torch.nn.DataParallel):
            model_state = model_state_to_cpu(model.module.state_dict())
        else:
            model_state = model.state_dict()
    else:
        model_state = None

    return {'epoch': epoch, 'model_state': model_state, 'optimizer_state': optim_state, 'best_result': best_result, 'best_epoch': best_epoch}


def save_checkpoint(state, filename):
    filename = '{}.pth'.format(filename)
    torch.save(state, filename)


def load_checkpoint(model, optimizer, filename, map_location, logger=None):
    if os.path.isfile(filename):
        logger.info("==> Loading from checkpoint '{}'".format(filename))
        checkpoint = torch.load(filename, map_location=map_location, weights_only=False) ##안전목록 추가 없이도 로드 성공
        epoch = checkpoint.get('epoch', -1)
        best_result = checkpoint.get('best_result', 0.0)
        best_epoch = checkpoint.get('best_epoch', 0.0)
        if model is not None and checkpoint.get('model_state') is not None:
            state = checkpoint['model_state']
            try:
                model.load_state_dict(state, strict=False)
            except Exception:
                # 만약 DataParallel 래핑 등으로 키 mismatch 나면
                if hasattr(model, 'module'):
                    model.module.load_state_dict(state, strict=False)
                else:
                    raise


    return epoch, best_result, best_epoch