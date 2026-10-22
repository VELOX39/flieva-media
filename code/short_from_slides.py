"""Turn a 9:16 slide set into a YouTube Short / reel: each slide holds, gentle zoom, whoosh between."""
import sys, subprocess
from socialkit import Timeline, music, sfx, SR
prefix, out, hold = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 3.2
import glob
files = sorted(glob.glob(f'out/{prefix}_*.jpg'), key=lambda f: int(f.rsplit('_', 1)[1].split('.')[0]))
total = hold * len(files)
tl = Timeline(total)
tl.add(0, music('upbeat', total, bpm=118), 0.8)
tl.add(0.05, sfx('boom'), 0.8)
for i in range(1, len(files)):
    tl.add(i * hold - 0.15, sfx('whoosh'), 0.9)
tl.write('out/_short.wav')
inputs, filt = [], []
for i, f in enumerate(files):
    inputs += ['-loop', '1', '-t', str(hold), '-i', f]
    filt.append(f"[{i}:v]scale=1080:1920,zoompan=z='1+0.0006*on':d={int(hold*30)}:s=1080x1920:fps=30,setsar=1[v{i}]")
filt.append(''.join(f'[v{i}]' for i in range(len(files))) + f'concat=n={len(files)}:v=1:a=0[v]')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *inputs, '-i', 'out/_short.wav', '-filter_complex', ';'.join(filt),
                '-map', '[v]', '-map', f'{len(files)}:a', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
                '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
print(out, total)
