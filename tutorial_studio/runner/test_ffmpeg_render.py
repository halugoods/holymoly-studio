import subprocess
import time
from pathlib import Path

def test_render():
    grid_mp4 = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/grid_loop_60fps.mp4")
    screen_mp4 = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fnb_catalog_24s_synced.mp4")
    mask_png = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/screen_mask_700x1710.png")
    frame_png = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/zflip3_frame.png")
    out_mp4 = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/test_ffmpeg_out.mp4")

    filter_complex = (
        "[1:v]fps=60,scale=700:1710:flags=lanczos[scaled_screen];"
        "[scaled_screen][2:v]alphamerge[masked_screen];"
        "[0:v][masked_screen]overlay=x=190:y=105[bg_screen];"
        "[bg_screen][3:v]overlay=x=0:y=0[final_v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(grid_mp4),
        "-i", str(screen_mp4),
        "-loop", "1", "-i", str(mask_png),
        "-loop", "1", "-i", str(frame_png),
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-map", "1:a?",
        "-t", "5",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(out_mp4)
    ]

    print("[FFmpeg] Testing 5s render with -loop 1...")
    t0 = time.perf_counter()
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    t1 = time.perf_counter()
    
    if res.returncode != 0:
        print("[FFmpeg Error]", res.stderr)
        return False
    
    print(f"[FFmpeg] SUCCESS! 5s rendered in {t1 - t0:.2f}s ({out_mp4.stat().st_size / (1024*1024):.2f} MB)")
    return True

if __name__ == "__main__":
    test_render()
