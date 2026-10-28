import cv2

img = cv2.imread("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744/verify_ep3_mockup_end.png")
print("Full Canvas:", img.shape)
# Center of canvas is (960, 540)
# Inside phone:
# Phone screen bounds: y=105 to 1815, x=190 to 890
print("Center receipt area (y=880, x=540):", img[880, 540])
print("Background grid area (y=500, x=100):", img[500, 100])
