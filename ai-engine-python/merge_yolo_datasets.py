import os
import shutil
import glob

# -------------- CONFIG -------------- #

# Each dataset folder must have: train/images, train/labels, valid/images, valid/labels
DATASETS = [
    {
        "name": "vehicle",
        "path": "datasets/vehicle",
        "classes": ['auto rickshaw', 'bus', 'car', 'motorbike', 'truck']
    },
    {
        "name": "pothole",
        "path": "datasets/pothole",
        "classes": ['pothole']
    },
    {
        "name": "person",
        "path": "datasets/person",
        "classes": ['person']
    },
    {
        "name": "animals",
        "path": "datasets/animals",
        "classes": ['cat', 'chicken', 'cow', 'dog', 'fox', 'goat', 'horse', 'person', 'racoon', 'skunk']
    },
    {
        "name": "speedbreaker",
        "path": "datasets/speedbreaker",
        "classes": ['SpeedBreaker']
    }
]

MERGED_ROOT = "datasets/merged"
SPLITS = ["train", "valid", "test"]  # 'test' optional

# -------------- HELPERS -------------- #

def ensure_dirs():
    """Create merged dataset folders with YOLO structure."""
    for split in SPLITS:
        os.makedirs(os.path.join(MERGED_ROOT, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(MERGED_ROOT, split, "labels"), exist_ok=True)

def merge_datasets():
    ensure_dirs()

    # Build global class list
    all_classes = []
    for d in DATASETS:
        for c in d["classes"]:
            if c not in all_classes:
                all_classes.append(c)
    print("🧩 Final class list:", all_classes)

    # Map dataset-specific IDs to global IDs
    class_map = {}
    for d in DATASETS:
        class_map[d["name"]] = {}
        for i, c in enumerate(d["classes"]):
            class_map[d["name"]][i] = all_classes.index(c)

    # Merge each dataset
    for d in DATASETS:
        name = d["name"]
        print(f"\n🚀 Merging dataset: {name}")
        for split in SPLITS:
            img_src = os.path.join(d["path"], split, "images")
            lbl_src = os.path.join(d["path"], split, "labels")

            if not os.path.exists(img_src):
                continue

            for img_path in glob.glob(f"{img_src}/*.*"):
                img_name = os.path.basename(img_path)
                lbl_name = os.path.splitext(img_name)[0] + ".txt"
                lbl_path = os.path.join(lbl_src, lbl_name)

                # Destination paths in YOLO-standard format
                img_dest = os.path.join(MERGED_ROOT, split, "images", img_name)
                lbl_dest = os.path.join(MERGED_ROOT, split, "labels", lbl_name)

                shutil.copy(img_path, img_dest)

                # Remap label IDs
                if os.path.exists(lbl_path):
                    with open(lbl_path, "r") as f:
                        lines = f.readlines()
                    new_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) < 5:
                            continue
                        old_cls = int(parts[0])
                        new_cls = class_map[name].get(old_cls)
                        if new_cls is not None:
                            parts[0] = str(new_cls)
                            new_lines.append(" ".join(parts) + "\n")
                    with open(lbl_dest, "w") as f:
                        f.writelines(new_lines)

    # Write final data.yaml
    yaml_path = os.path.join(MERGED_ROOT, "data.yaml")
    with open(yaml_path, "w") as f:
        f.write(f"train: {MERGED_ROOT}/train/images\n")
        f.write(f"val: {MERGED_ROOT}/valid/images\n")
        f.write(f"test: {MERGED_ROOT}/test/images\n\n")
        f.write(f"nc: {len(all_classes)}\n")
        f.write(f"names: {all_classes}\n")

    print(f"\n✅ Merged dataset ready at {MERGED_ROOT}")
    print(f"YAML path: {yaml_path}")

# -------------- MAIN -------------- #

if __name__ == "__main__":
    merge_datasets()
