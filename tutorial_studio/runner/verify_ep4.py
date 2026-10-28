import subprocess
import shutil
from pathlib import Path

video = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio\tutorial_studio\output\bengkel_servis_21s_motion_commercial.mp4")
out_dir = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")

dest_video = out_dir / "ep4_bengkel_servis_commercial.mp4"
shutil.copyfile(str(video), str(dest_video))
print(f"Copied {video.name} -> {dest_video} ({dest_video.stat().st_size / (1024*1024):.2f} MB)")

timestamps = ["00:00:02.000", "00:00:06.000", "00:00:09.000", "00:00:12.800", "00:00:18.000"]
labels = ["02s", "06s", "09s", "13s", "18s"]
for ts, lbl in zip(timestamps, labels):
    frame_path = out_dir / f"f_ep4_{lbl}.png"
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", str(video), "-vframes", "1", str(frame_path)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted frame at {ts} -> {frame_path.name}")
