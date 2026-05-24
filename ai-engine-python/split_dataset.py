import os
import random
import shutil
import time

# ✅ Base dataset path
base_dir = "datasets/night.v1i.yolov11"  # change if needed

# Original test folder (currently holding all data)
src_img_dir = os.path.join(base_dir, "test1", "images")
src_lbl_dir = os.path.join(base_dir, "test1", "labels")

# Destination folder structure
splits = ["train", "valid", "test"]
for split in splits:
    os.makedirs(os.path.join(base_dir, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, split, "labels"), exist_ok=True)

# ✅ Ratios for splitting
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1  # remaining 10%

# ✅ Get all image files
images = [f for f in os.listdir(src_img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(images)

# ✅ Split dataset
n = len(images)
train_imgs = images[:int(n * train_ratio)]
val_imgs = images[int(n * train_ratio):int(n * (train_ratio + val_ratio))]
test_imgs = images[int(n * (train_ratio + val_ratio)):]

def safe_copy(src, dest, retries=3, delay=0.5):
    """Safely copy files, retry if file is temporarily locked."""
    for attempt in range(retries):
        try:
            shutil.copy2(src, dest)
            return True
        except PermissionError:
            print(f"⚠️ File locked: {os.path.basename(src)} — retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Error copying {src}: {e}")
            return False
    print(f"❌ Skipping {src}, file still locked after retries.")
    return False

def move_files(img_list, split):
    dest_img_dir = os.path.join(base_dir, split, "images")
    dest_lbl_dir = os.path.join(base_dir, split, "labels")

    for img_name in img_list:
        src_img_path = os.path.join(src_img_dir, img_name)
        lbl_name = os.path.splitext(img_name)[0] + ".txt"
        src_lbl_path = os.path.join(src_lbl_dir, lbl_name)

        dest_img_path = os.path.join(dest_img_dir, img_name)
        dest_lbl_path = os.path.join(dest_lbl_dir, lbl_name)

        if os.path.exists(src_img_path):
            safe_copy(src_img_path, dest_img_path)
        if os.path.exists(src_lbl_path):
            safe_copy(src_lbl_path, dest_lbl_path)

# ✅ Move to each split
move_files(train_imgs, "train")
move_files(val_imgs, "valid")
move_files(test_imgs, "test")

# ✅ Delete the old test folder (source)


print("✅ Dataset split completed successfully!")
print(f"Train: {len(train_imgs)} images")
print(f"Valid: {len(val_imgs)} images")
print(f"Test: {len(test_imgs)} images")
