import os
import shutil
import yaml

# --- Paths ---
base = r"C:\Users\TEJAS\Documents\NightVision\ai-engine-python\datasets"
src_dir = os.path.join(base, "merged_V2")
dest_dir = os.path.join(base, "merged_V3")

# --- Create new structure ---
for split in ["train", "valid", "test"]:
    os.makedirs(os.path.join(dest_dir, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, split, "labels"), exist_ok=True)

# --- Class index mapping from merged_V2 ---
AUTO_RICKSHAW_IDX = 0
CAR_IDX = 2  # original index before merge

# --- Copy and modify ---
for split in ["train", "valid", "test"]:
    src_img_dir = os.path.join(src_dir, split, "images")
    src_lbl_dir = os.path.join(src_dir, split, "labels")
    dest_img_dir = os.path.join(dest_dir, split, "images")
    dest_lbl_dir = os.path.join(dest_dir, split, "labels")

    for file in os.listdir(src_img_dir):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Copy image
        shutil.copy2(os.path.join(src_img_dir, file), os.path.join(dest_img_dir, file))

        # Label path
        lbl_name = os.path.splitext(file)[0] + ".txt"
        src_lbl_path = os.path.join(src_lbl_dir, lbl_name)
        dest_lbl_path = os.path.join(dest_lbl_dir, lbl_name)

        if not os.path.exists(src_lbl_path):
            open(dest_lbl_path, "w").close()
            continue

        # Read & process label lines
        with open(src_lbl_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            cls = int(parts[0])

            # Merge auto rickshaw → car
            if cls == AUTO_RICKSHAW_IDX:
                cls = CAR_IDX

            # Reduce all class indices by 1
            cls = cls - 1

            new_lines.append(f"{cls} " + " ".join(parts[1:]) + "\n")

        # Write modified label
        with open(dest_lbl_path, "w") as f:
            f.writelines(new_lines)

    print(f"✅ Finished processing {split}")

# --- Update YAML ---
yaml_src = os.path.join(src_dir, "data.yaml")
yaml_dest = os.path.join(dest_dir, "data.yaml")

with open(yaml_src, "r") as f:
    data = yaml.safe_load(f)

# Remove 'auto rickshaw' and shift indices
if "auto rickshaw" in data["names"]:
    data["names"].remove("auto rickshaw")

# Update class count
data["nc"] = len(data["names"])

# Update paths
data["train"] = os.path.join(dest_dir, "train/images").replace("\\", "/")
data["val"] = os.path.join(dest_dir, "valid/images").replace("\\", "/")
data["test"] = os.path.join(dest_dir, "test/images").replace("\\", "/")

# Save updated YAML
with open(yaml_dest, "w") as f:
    yaml.dump(data, f, sort_keys=False)

print("\n🎉 Merge complete!")
print(f"📁 Saved new dataset: {dest_dir}")
print(f"🧾 Updated YAML: {yaml_dest}")
