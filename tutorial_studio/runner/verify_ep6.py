import subprocess
import shutil
from pathlib import Path

video = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio\tutorial_studio\output\salon_treatment_19s_motion_commercial.mp4")
out_dir = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")

dest_video = out_dir / "ep6_salon_treatment_commercial.mp4"
shutil.copyfile(str(video), str(dest_video))
print(f"Copied {video.name} -> {dest_video} ({dest_video.stat().st_size / (1024*1024):.2f} MB)")

timestamps = ["00:00:02.000", "00:00:05.500", "00:00:08.500", "00:00:11.800", "00:00:16.500"]
labels = ["02s", "05s", "08s", "12s", "16s"]
for ts, lbl in zip(timestamps, labels):
    frame_path = out_dir / f"f_ep6_{lbl}.png"
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", str(video), "-vframes", "1", str(frame_path)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted frame at {ts} -> {frame_path.name}")
