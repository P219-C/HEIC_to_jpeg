import os
import subprocess
from pathlib import Path
from PIL import Image
import pillow_heif

# Enable HEIC support in Pillow
pillow_heif.register_heif_opener()

INPUT_DIR = Path("L:\\INPUT\\PATH")
OUTPUT_DIR = Path("L:\\OUTPUT\\PATH")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def convert_heic_to_jpeg_with_metadata(src_path: Path, dst_path: Path, quality=95):
    # Open HEIC and save as JPEG
    with Image.open(src_path) as img:
        rgb_img = img.convert("RGB")
        rgb_img.save(dst_path, "JPEG", quality=quality)

    print("Image Conversion good")
    # Copy all metadata from source to destination
    # -overwrite_original: don't create backup
    # -TagsFromFile: copy tags from source
    # -all:all: copy all metadata groups where possible
    result = subprocess.run(
        [
            ".\\third_party\\exiftool-13.53_64\\exiftool",
            "-overwrite_original",
            "-TagsFromFile", str(src_path),
            "-all:all",
            str(dst_path),
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"ExifTool failed for {src_path}:\n{result.stderr}")

def batch_convert():
    for src_path in INPUT_DIR.glob("*.HEIC"):
        dst_path = OUTPUT_DIR / (src_path.stem + ".jpg")
        print(f"Converting {src_path} -> {dst_path}")
        try:
            convert_heic_to_jpeg_with_metadata(src_path, dst_path)
        except Exception as e:
            print(f"Failed: {src_path}: {e}")

if __name__ == "__main__":
    batch_convert()