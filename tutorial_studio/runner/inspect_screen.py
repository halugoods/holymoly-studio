import cv2
import sys

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "output/laundry_start.png"
    img = cv2.imread(path)
    if img is None:
        print("Failed to read", path)
        return
    print(f"Loaded {path}: {img.shape[1]}x{img.shape[0]} channels: {img.shape[2]}")

if __name__ == "__main__":
    main()
