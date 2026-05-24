import os
import shutil
import yaml

# --- Paths ---
base = r"C:\Users\TEJAS\Documents\NightVision\ai-engine-python\datasets"
merged_dir = os.path.join(base, "merged_V2")

datasets = [
    os.path.join(base, "merged"),
    os.path.join(base, "night cars.v3i.yolov11"),
    os.path.join(base, "night.v1i.yolov11"),
]

# --- Unified Class List ---
CLASS_NAMES = [
    'auto rickshaw', 'bus', 'car', 'motorbike', 'truck',
    'pothole', 'person', 'cat', 'chicken', 'cow',
    'dog', 'fox', 'goat', 'horse', 'racoon', 'skunk', 'SpeedBreaker'
]

# --- Name normalization across datasets ---
NAME_NORMALIZATION = {
    'motobike': 'motorbike',
    'bicyclist': 'motorbike',
    'ele_motorcyclist': 'motorbike',
    'pedestrian': 'person',
    'tricycle': 'auto rickshaw',
    'vehicle': 'car'
}

# --- Create merged directories ---
os.makedirs(merged_dir, exist_ok=True)
for split in ["train", "valid", "test"]:
    os.makedirs(os.path.join(merged_dir, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(merged_dir, split, "labels"), exist_ok=True)

# --- Helper functions ---
def load_dataset_yaml(dataset_path):
    yaml_path = os.path.join(dataset_path, "data.yaml")
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            return yaml.safe_load(f)
    return None

def convert_label(label_path, dest_label_path, class_map):
    """Convert labels using dataset-specific index→name→unified index mapping."""
    with open(label_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        old_idx_str = parts[0]

        # Determine old class name
        try:
            old_idx = int(old_idx_str)
            old_name = class_map.get(old_idx, None)
        except:
            old_name = old_idx_str  # maybe string

        if old_name is None:
            continue

        old_name = old_name.lower().strip()
        # Normalize variants
        if old_name in NAME_NORMALIZATION:
            old_name = NAME_NORMALIZATION[old_name]

        # Map to unified index
        try:
            new_idx = [i for i, n in enumerate(CLASS_NAMES) if n.lower() == old_name][0]
        except IndexError:
            # Class not in unified list → skip
            continue

        new_lines.append(f"{new_idx} " + " ".join(parts[1:]) + "\n")

    # Save new label
    with open(dest_label_path, "w") as f:
        f.writelines(new_lines)

def copy_dataset(dataset_path):
    """Copy dataset images + relabel, handling missing labels."""
    dataset_yaml = load_dataset_yaml(dataset_path)
    if dataset_yaml and "names" in dataset_yaml:
        class_map = {i: name for i, name in enumerate(dataset_yaml["names"])}
    else:
        class_map = {}

    missing_labels = []

    for split in ["train", "valid", "test"]:
        img_dir = os.path.join(dataset_path, split, "images")
        lbl_dir = os.path.join(dataset_path, split, "labels")

        if not os.path.exists(img_dir):
            continue

        for img_name in os.listdir(img_dir):
            if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            src_img = os.path.join(img_dir, img_name)
            src_lbl = os.path.join(lbl_dir, os.path.splitext(img_name)[0] + ".txt")

            dest_img = os.path.join(merged_dir, split, "images", img_name)
            dest_lbl = os.path.join(merged_dir, split, "labels", os.path.splitext(img_name)[0] + ".txt")

            shutil.copy2(src_img, dest_img)

            if os.path.exists(src_lbl):
                convert_label(src_lbl, dest_lbl, class_map)
            else:
                # Create empty label file if missing
                open(dest_lbl, "w").close()
                missing_labels.append(dest_lbl)

    if missing_labels:
        print(f"⚠️ {len(missing_labels)} missing label files created in {dataset_path}")

# --- Merge all datasets ---
for d in datasets:
    print(f"🔄 Processing {d} ...")
    copy_dataset(d)

# --- Create final data.yaml ---
data_yaml = {
    'train': os.path.join(merged_dir, 'train/images').replace("\\", "/"),
    'val': os.path.join(merged_dir, 'valid/images').replace("\\", "/"),
    'test': os.path.join(merged_dir, 'test/images').replace("\\", "/"),
    'nc': len(CLASS_NAMES),
    'names': CLASS_NAMES
}

yaml_path = os.path.join(merged_dir, 'data.yaml')
with open(yaml_path, 'w') as f:
    yaml.dump(data_yaml, f, sort_keys=False)

print("✅ Merging complete. Final YAML written to:", yaml_path)
