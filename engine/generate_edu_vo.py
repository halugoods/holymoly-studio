import urllib.request
import json
import base64
import os
import subprocess

API_KEY = os.environ.get('GEMINI_API_KEY', '')
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}'

text = (
    "Dalam waktu nol koma satu detik saat kamu melihat sesuatu, "
    "delapan puluh enam miliar neuron di otakmu langsung menyala. "
    "Seratus triliun sinapsis mengirim sinyal listrik dengan kecepatan empat ratus kilometer per jam, "
    "membentuk apa yang kita sebut sebuah ingatan."
)

prompt_instruction = (
    "Bicara seperti narator dokumenter sains modern kelas dunia, "
    "nada tenang, berwibawa, artikulatif, tempo santai dengan jeda napas alami: " + text
)

payload = {
    'contents': [{'parts': [{'text': prompt_instruction}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO'],
        'speechConfig': {
            'voiceConfig': {
                'prebuiltVoiceConfig': {
                    'voiceName': 'Aoede'
                }
            }
        }
    }
}

print("Generating Educational Narration via Gemini TTS (Aoede)...")
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
out_pcm = r'C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744\edu_brain_vo_raw.pcm'
out_wav = r'C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744\edu_brain_vo.wav'

with urllib.request.urlopen(req, timeout=30) as resp:
    res_data = json.loads(resp.read().decode('utf-8'))
    audio_b64 = res_data['candidates'][0]['content']['parts'][0]['inlineData']['data']
    audio_bytes = base64.b64decode(audio_b64)
    with open(out_pcm, 'wb') as f:
        f.write(audio_bytes)
    print(f"Downloaded {len(audio_bytes)} raw PCM bytes.")

# Convert to wav
cmd = f'ffmpeg -f s16le -ar 24000 -ac 1 -i "{out_pcm}" -c:a pcm_s16le "{out_wav}" -y'
subprocess.run(cmd, shell=True, check=True)

# Probe duration
probe = subprocess.run(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{out_wav}"', shell=True, capture_output=True, text=True)
dur = float(probe.stdout.strip())
print(f"Generated clean educational voiceover: {out_wav} (Duration: {dur:.2f}s)")
