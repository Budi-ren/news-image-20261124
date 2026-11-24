import os
import shutil

def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    dest_path = os.path.join(output_dir, "entry.png")
    src = os.path.join(os.path.dirname(__file__), "entry.png")
    shutil.copy(src, dest_path)
    os.chmod(dest_path, 0o644)

if __name__ == "__main__":
    main()
