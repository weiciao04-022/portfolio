"""離線更新素材：python3 scripts/prepare-room.py /圖片資料夾 [張數=800]
需要 Pillow，以及系統 ffmpeg 或 imageio-ffmpeg。網站本身不需要 Python。
"""
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image

source = Path(sys.argv[1])
count = int(sys.argv[2]) if len(sys.argv) > 2 else 800
output = Path(__file__).resolve().parents[1] / 'assets' / 'room'
output.mkdir(parents=True, exist_ok=True)
for frame in range(1, count + 1):
    if not (source / f'Room_{frame:04}.png').is_file():
        raise SystemExit(f'缺少 Room_{frame:04}.png，未更新素材')
encoder = shutil.which('ffmpeg')
if not encoder:
    from imageio_ffmpeg import get_ffmpeg_exe
    encoder = get_ffmpeg_exe()
subprocess.run([encoder, '-y', '-framerate', '24', '-start_number', '1',
    '-i', str(source / 'Room_%04d.png'), '-frames:v', str(count),
    '-c:v', 'libx264', '-preset', 'fast',
    '-crf', '16', '-pix_fmt', 'yuv420p', '-g', '24', '-movflags', '+faststart',
    str(output / 'tour.mp4')], check=True)
for name, frame in [('home', 1), ('cabinet', 192), ('bookshelf', 396),
                    ('newspaper', 552), ('laptop', 684)]:
    if frame <= count:
        with Image.open(source / f'Room_{frame:04}.png') as image:
            image.convert('RGB').save(output / f'{name}.webp', lossless=True, method=6)
