#!/usr/bin/env python3
"""Validate this repository's conservative 48-channel FSEQ profile; not all FSEQ."""
import argparse
import json
from pathlib import Path
import struct
import wave

RAMPS = {0, 25, 51, 76, 178, 204, 229, 255}
RAMP_CHANNELS = {3, 4, 7, 8, 11, 12, 13, 14}
MUSICAL_CHANNELS = {3, 4, 7, 8, 11, 13, 14, 21, 22, 23, 24, 25, 26, 27}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(path, audio=None, musical=False):
    raw = Path(path).read_bytes()
    require(len(raw) >= 32, 'Truncated header')
    require(raw[:4] == b'PSEQ', 'Expected PSEQ signature')
    offset, minor, major, header, channels, frames, step = struct.unpack_from('<HBBHIIB', raw, 4)
    require((offset, minor, major, header, channels, step) == (32, 0, 2, 32, 48, 20), 'Unsupported profile: expected minimal FSEQ 2.0, 48 channels, 20 ms')
    require(not any(raw[19:32]), 'Optional/header fields must be zero in this profile')
    require(5 <= frames <= 720000, 'Frame count outside profile limits')
    require(len(raw) == 32 + frames * channels, 'Payload size mismatch')
    data = raw[32:]
    require(not any(data[-5 * channels:]), 'Last 100 ms must be dark')
    stats = {}
    streams = {}
    for c in range(1, 49):
        x = data[c - 1::48]
        streams[c] = x
        values = set(x)
        require(values <= (RAMPS if c in RAMP_CHANNELS else {0, 255}), f'Unsupported command on channel {c}')
        if c >= 31:
            require(not any(x), f'Mechanical/reserved channel {c} active')
        if musical:
            require(c in MUSICAL_CHANNELS or not any(x), f'Channel {c} outside musical profile')
        onsets = sum(v != 0 and (i == 0 or x[i - 1] == 0) for i, v in enumerate(x))
        stats[c] = dict(active_seconds=round(sum(v != 0 for v in x) * .02, 2), onsets=onsets, values=sorted(values))
    if musical:
        for c in [7, 8, 11, 13, 14, 23, 24]:
            require(any(streams[c]), f'Required channel {c} inactive')
        for c in [13, 14, 23, 24]:
            x = streams[c]
            require(stats[c]['onsets'] >= 8, f'Channel {c} requires at least eight onsets in a full musical show')
            boundaries = [0] + [i for i in range(1, frames) if bool(x[i]) != bool(x[i-1])] + [frames]
            for a, b in zip(boundaries, boundaries[1:]):
                if x[a] or (a > 0 and b < frames):
                    require(b-a >= 5, f'Channel {c}: pulse/internal gap shorter than 100 ms')
        for white, amber in [(7, 13), (8, 14)]:
            require(not any(a and b for a, b in zip(streams[white], streams[amber])), f'White/amber overlap: {white}/{amber}')
        require(streams[7] != streams[11] and streams[8] != streams[11], 'Center and side streams must differ')
    duration = frames * .02
    if audio:
        with wave.open(str(audio), 'rb') as w:
            require(w.getcomptype() == 'NONE' and w.getsampwidth() == 2 and w.getframerate() == 44100 and w.getnchannels() in [1, 2], 'Expected mono/stereo PCM16 WAV at 44100 Hz')
            require(abs(w.getnframes()/44100-duration) <= .020001, 'Audio duration differs by more than one frame')
    return dict(profile='juniper-minimal-48', frames=frames, duration_seconds=duration, musical=musical, channels=stats, physical_playback='not verified by this tool')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('fseq', type=Path)
    p.add_argument('--audio', type=Path)
    p.add_argument('--musical', action='store_true')
    args = p.parse_args()
    try:
        print(json.dumps(validate(args.fseq, args.audio, args.musical), indent=2))
    except (ValueError, OSError, wave.Error, EOFError) as error:
        p.exit(1, f'Validation failed: {error}\n')


if __name__ == '__main__':
    main()
