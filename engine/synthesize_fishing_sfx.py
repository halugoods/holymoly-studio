import numpy as np
import wave
import struct

SAMPLE_RATE = 44100

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    # Normalize to -1.0 to 1.0, then convert to 16-bit PCM
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767).astype(np.int16)
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())
    print(f"Saved {filename} ({len(samples)/sample_rate:.2f}s)")

def generate_reel_drag(duration=4.0, click_rate=55, sample_rate=SAMPLE_RATE):
    """Synthesizes realistic screaming reel drag clicker."""
    total_samples = int(duration * sample_rate)
    audio = np.zeros(total_samples)
    
    # Each click is a sharp resonant pop at ~4200 Hz decaying in 4ms
    click_len = int(0.005 * sample_rate)
    t_click = np.linspace(0, 0.005, click_len)
    click = np.sin(2 * np.pi * 4200 * t_click) * np.exp(-t_click * 1000)
    # Add slight click variation/snappiness
    click += 0.5 * np.sin(2 * np.pi * 2800 * t_click) * np.exp(-t_click * 1200)
    
    # Place clicks at click_rate per second with slight human jitter
    step = sample_rate / click_rate
    pos = 0.0
    while pos + click_len < total_samples:
        idx = int(pos)
        audio[idx:idx+click_len] += click * (0.8 + 0.4 * np.random.rand())
        # Jitter the drag speed slightly
        jitter = (np.random.rand() - 0.5) * (step * 0.25)
        pos += step + jitter
        
    return audio

def generate_water_splash(duration=2.5, sample_rate=SAMPLE_RATE):
    """Synthesizes explosive surface water splash."""
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples)
    
    # Low-end boom / impact thump
    thump = np.sin(2 * np.pi * (80 - 40 * t) * t) * np.exp(-t * 6.0)
    
    # White noise filtered burst for the foaming splash
    noise = np.random.randn(total_samples)
    # Fast attack, smooth decay
    envelope = np.exp(-t * 3.5) * (1 - np.exp(-t * 80))
    splash = noise * envelope * 0.7
    
    combined = thump * 0.8 + splash * 0.7
    return combined

def generate_ambience(duration=18.0, sample_rate=SAMPLE_RATE):
    """Subtle nature river atmosphere."""
    total_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, total_samples)
    
    # Gentle low rumble / river movement
    rumble = np.sin(2 * np.pi * 55 * t) * 0.03
    # Gentle high cicada shimmer
    shimmer = np.sin(2 * np.pi * 6500 * t) * 0.015 * (1 + 0.5 * np.sin(2 * np.pi * 8 * t))
    
    noise = np.random.randn(total_samples) * 0.02
    return rumble + shimmer + noise

if __name__ == '__main__':
    out_dir = r'C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744'
    drag = generate_reel_drag(duration=4.0, click_rate=60)
    splash = generate_water_splash(duration=2.5)
    amb = generate_ambience(duration=18.0)
    
    save_wav(f"{out_dir}\\sfx_reel_drag.wav", drag)
    save_wav(f"{out_dir}\\sfx_water_splash.wav", splash)
    save_wav(f"{out_dir}\\sfx_river_ambience.wav", amb)
