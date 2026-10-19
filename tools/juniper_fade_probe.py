#!/usr/bin/env python3
"""Reproduce isolated Juniper fade commands. Python 3 standard library; MIT license.
One-based channels. No closures. Exact generated file awaits vehicle testing.
"""
import argparse
import array
import json
import math
from pathlib import Path
import struct
import sys
import wave


def build(output):
    root = Path(output)
    folder = root / 'LightShow'
    folder.mkdir(parents=True, exist_ok=True)
    name = 'juniper_fade_probe'
    destinations = [folder / (name + ext) for ext in ('.fseq', '.wav')]
    timeline_file = root / 'timeline.json'
    if any(p.exists() for p in destinations + [timeline_file]):
        raise FileExistsError('Output already exists; choose a new --output directory')
    channels, frames, step, duration = 48, 2550, 20, 51
    data = bytearray(channels * frames)
    timeline = []

    def command(chs, start, end, value):
        a, b = round(start * 50), round(end * 50)
        assert 0 <= a < b <= frames
        for frame in range(a, b):
            for channel in chs:
                data[frame * channels + channel - 1] = value
        timeline.append(dict(channels=chs, start=a / 50, end=b / 50, byte=value))

    groups = [[11], [12], [11, 12], [7, 8, 11, 12]]
    for i, chs in enumerate(groups):
        t = 2 + i * 12
        command(chs, t, t + .4, 255)
        for offset, seconds, on, off in [(1, 1, 204, 51), (4, 2, 229, 76), (9, .5, 178, 25)]:
            start = t + offset
            middle = start + seconds + .06
            command(chs, start, middle, on)
            command(chs, middle, middle + seconds + .06, off)
    header = bytearray(32)
    header[:4] = b'PSEQ'
    struct.pack_into('<HBBHIIB', header, 4, 32, 0, 2, 32, channels, frames, step)
    destinations[0].write_bytes(header + data)
    sr = 44100
    audio = array.array('h', [0]) * (duration * sr)
    for i in range(4):
        start = (2 + i * 12) * sr
        length = round(.2 * sr)
        for n in range(length):
            audio[start + n] = round(15000 * math.sin(2 * math.pi * (660 + 110*i) * n / sr) * math.sin(math.pi*n/length)**2)
    if sys.byteorder != 'little':
        audio.byteswap()
    with wave.open(str(destinations[1]), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(audio.tobytes())
    timeline_file.write_text(json.dumps(timeline, indent=2), encoding='utf-8')
    saved = destinations[0].read_bytes()
    assert len(saved) == 32 + frames * channels
    assert saved[:4] == b'PSEQ' and saved[20] == 0
    assert not any(data[-48 * 50:])
    for frame in range(frames):
        assert not any(data[frame*48+30:frame*48+48])
    assert set(data) <= {0, 25, 51, 76, 178, 204, 229, 255}
    with wave.open(str(destinations[1])) as w:
        assert w.getnframes() / w.getframerate() == frames * step / 1000
    print('Created and structurally checked:', *destinations, sep='\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='juniper_probe')
    build(parser.parse_args().output)
