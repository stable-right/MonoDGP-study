# iou_backend.py (OpenCV 기반 Rotated IoU: CPU)
import math
import numpy as np
import cv2

# --- 유틸: 라디안(CW, +) -> 도(CCW, +) 변환
def rad_cw_to_deg_ccw(rad):
    return float(-rad * 180.0 / math.pi)

# --- 유틸: 회전 사각형(rbox) -> 꼭짓점 4점 폴리곤
def rbox_to_poly(cx, cy, w, h, angle_deg):
    # angle_deg: degree, CCW(+). OpenCV boxPoints와 동일 기준
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    dx, dy = w / 2.0, h / 2.0
    pts = np.array([[-dx, -dy], [dx, -dy], [dx, dy], [-dx, dy]], dtype=np.float32)
    R = np.array([[c, -s], [s,  c]], dtype=np.float32)
    rot = (R @ pts.T).T
    rot[:, 0] += cx
    rot[:, 1] += cy
    return rot.astype(np.float32)

def poly_area(poly):
    return float(cv2.contourArea(poly.astype(np.float32)))

# --- (도, CCW) 기준의 일반 IoU 계산기
def iou_rotated_deg(boxes1_deg, boxes2_deg, criterion=-1):
    """
    boxes*_deg: (N,5)/(M,5) with columns [cx, cy, w, h, angle_deg(CCW)]
    criterion: -1 IoU, 0 IoF(gt), 1 IoF(dt), other => return intersection area
    """
    N = int(boxes1_deg.shape[0])
    M = int(boxes2_deg.shape[0])
    out = np.zeros((N, M), dtype=np.float32)
    for i in range(N):
        cx1, cy1, w1, h1, a1 = map(float, boxes1_deg[i])
        p1 = rbox_to_poly(cx1, cy1, w1, h1, a1)
        A1 = abs(poly_area(p1))
        for j in range(M):
            cx2, cy2, w2, h2, a2 = map(float, boxes2_deg[j])
            p2 = rbox_to_poly(cx2, cy2, w2, h2, a2)
            A2 = abs(poly_area(p2))
            inter, _ = cv2.intersectConvexConvex(p1, p2)
            inter = float(inter) if inter is not None else 0.0
            if criterion == -1:       # IoU
                denom = A1 + A2 - inter
            elif criterion == 0:      # IoF(gt)
                denom = A1
            elif criterion == 1:      # IoF(dt)
                denom = A2
            else:                     # just return intersection
                out[i, j] = inter
                continue
            out[i, j] = inter / denom if denom > 0 else 0.0
    return out

# --- 레포의 호출 시그니처를 맞추는 래퍼 (라디안/CW -> 도/CCW 변환 포함)
def rotate_iou_gpu_eval(boxes, query_boxes, criterion=-1):
    """
    레포 쪽에서 호출하는 시그니처와 동일.
    입력 boxes, query_boxes는 (N,5)/(M,5) with [cx, cy, w, h, angle_rad(CW,+)] 라는 전제를 따른다.
    이걸 도/CCW로 변환해서 iou_rotated_deg로 계산.
    """
    if boxes.size == 0 or query_boxes.size == 0:
        return np.zeros((boxes.shape[0], query_boxes.shape[0]), dtype=np.float32)

    boxes = np.asarray(boxes, dtype=np.float32)
    query_boxes = np.asarray(query_boxes, dtype=np.float32)

    # 각도만 라디안(CW) -> 도(CCW) 변환
    boxes_deg = boxes.copy()
    query_deg = query_boxes.copy()
    boxes_deg[:, 4] = np.vectorize(rad_cw_to_deg_ccw)(boxes[:, 4])
    query_deg[:, 4] = np.vectorize(rad_cw_to_deg_ccw)(query_boxes[:, 4])

    return iou_rotated_deg(boxes_deg, query_deg, criterion)
