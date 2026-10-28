import subprocess
import shutil
from pathlib import Path

video = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio\tutorial_studio\output\laundry_kiloan_21s_motion_commercial.mp4")
out_dir = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")

# Copy video to artifact dir
dest_video = out_dir / "ep3_laundry_kiloan_commercial.mp4"
shutil.copyfile(str(video), str(dest_video))
print(f"Copied {video.name} -> {dest_video} ({dest_video.stat().st_size / (1024*1024):.2f} MB)")

# Extract sample frames for verification
timestamps = ["00:00:02.000", "00:00:07.000", "00:00:11.000", "00:00:15.000", "00:00:19.000"]
labels = ["02s", "07s", "11s", "15s", "19s"]
for ts, lbl in zip(timestamps, labels):
    frame_path = out_dir / f"f_ep3_{lbl}.png"
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", str(video), "-vframes", "1", str(frame_path)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted frame at {ts} -> {frame_path.name}")
