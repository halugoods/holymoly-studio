import cv2

img = cv2.imread(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744\f_mockup_preview.png")
# Check screen area: (190, 105) to (190+700, 105+1710)
screen_crop = img[105:105+1710, 190:190+700]
print("Screen crop shape:", screen_crop.shape)
# Check top status bar inside screen: (0 to 120 of screen_crop)
status_bar = screen_crop[0:100, :]
print("Status bar mean BGR:", status_bar.mean(axis=(0, 1)).astype(int))
