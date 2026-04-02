import os
import subprocess
from pathlib import Path
from PIL import Image
import pillow_heif
import tkinter as tk
from tkinter import filedialog

# Enable HEIC support in Pillow
pillow_heif.register_heif_opener()

def convert_heic_to_jpeg_with_metadata(src_path: Path, dst_path: Path, quality=95):
    # Open HEIC and save as JPEG
    with Image.open(src_path) as img:
        rgb_img = img.convert("RGB")
        rgb_img.save(dst_path, "JPEG", quality=quality)

    # Copy all metadata from source to destination
    # -overwrite_original: don't create backup
    # -TagsFromFile: copy tags from source
    # -all:all: copy all metadata groups where possible
    result = subprocess.run(
        [
            ".\\exiftool-13.53_64\\exiftool",
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
    

def listSpecificFiles(targetPath, targetExtension_or_targetExtensions):
    """Returns in a list all files contained in *path* and the subfolders"""
    print(f"CONFIRMATION: {targetExtension_or_targetExtensions}")
    if targetExtension_or_targetExtensions:
        print("\nLISTING SPECIFIC FILES")
        return [(file, os.path.getsize(file)) for file in Path(targetPath).rglob('*')
                if file.is_file() and file.suffix and file.suffix.lower() in targetExtension_or_targetExtensions]
    else:
        print("\nLISTING ALL FILES")
        return [(file, os.path.getsize(file)) for file in Path(targetPath).rglob('*')
                if file.is_file()]


def main_function():
    # Open window to select folder
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    target_directory = filedialog.askdirectory(title="Select a folder")

    target_extensions = ".heic"

    print(f"Extension to find: {target_extensions}")

    # Executing 'listSpecificFiles' function
    print("\nEXECUTING MAIN FUNCTION...")
    output_list = listSpecificFiles(target_directory, target_extensions)
    # print(*output_list, sep='\n')
    # print('\n'.join(f'[{i+1}/{len(output_list)}]: {os.path.basename(x[0])}, {x[0]}, [{x[1]} bytes]' for i, x in enumerate(output_list)))

    # Unpacking output_list
    fullPaths, fileSizes = zip(*output_list)

    for src_path in fullPaths:
        dst_path = Path(src_path).parent / (src_path.stem + ".jpg")
        print(f"_______: Converting {src_path} -> {dst_path}")
        try:
            convert_heic_to_jpeg_with_metadata(src_path, dst_path)
            print(f"SUCCESS: Converting {src_path} -> {dst_path}")
        except Exception as e:
            print(f"Failed: {src_path}: {e}")


if __name__ == "__main__":
    main_function()