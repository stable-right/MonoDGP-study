import os, random

image_dir = 'data/kitti/training/image_2'
images = sorted(os.listdir(image_dir))
image_ids = [img.split('.')[0] for img in images if img.endswith('.png')]

random.seed(42)
random.shuffle(image_ids)

train_ratio = 0.85
split_index = int(len(image_ids) * train_ratio)
train_ids, val_ids = image_ids[:split_index], image_ids[split_index:]

os.makedirs('data/kitti/ImageSets', exist_ok=True)
with open('data/kitti/ImageSets/train.txt', 'w') as f:
    f.write('\n'.join(train_ids))
with open('data/kitti/ImageSets/val.txt', 'w') as f:
    f.write('\n'.join(val_ids))
