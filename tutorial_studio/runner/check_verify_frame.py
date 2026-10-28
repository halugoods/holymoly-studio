import cv2

img = cv2.imread("holymoly_studio/tutorial_studio/output/verify_laundry_17s.png")
print("Image shape:", img.shape)
# Modal scrim background at (100, 100):
print("Scrim color at (100, 100):", img[100, 100])
# Center receipt card at (1200, 540):
print("Card color at (1200, 540):", img[1200, 540])
# Cetak Printer button at (1842, 540):
print("Button color at (1842, 540):", img[1842, 540])
# Share WA button at (1984, 311):
print("Share WA color at (1984, 311):", img[1984, 311])
