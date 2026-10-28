import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

for i in range(1, 9):
    fn = f"ep{i}_*.mp4"
    files = list(OUT_DIR.glob(fn))
    if not files:
        continue
    f = files[0]
    
    # Get duration
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(f)], stdout=subprocess.PIPE, text=True)
    dur = float(p.stdout.strip())
    
    # Extract frame at dur - 1.5s
    seek = max(0, dur - 1.5)
    out_frame = OUT_DIR / f"audit_end_ep{i}.png"
    subprocess.run(["ffmpeg", "-y", "-ss", str(seek), "-i", str(f), "-vframes", "1", str(out_frame)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"[Audit] EP{i} ({f.name}) duration: {dur:.2f}s, extracted end frame at {seek:.2f}s -> {out_frame.name}")
