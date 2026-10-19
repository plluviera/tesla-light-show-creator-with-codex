import contextlib
import io
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from juniper_fade_probe import build
from validate_show import validate


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'show.fseq'
        self.frames = 1000
        self.data = bytearray(48 * self.frames)

    def write(self):
        header = bytearray(32)
        header[:4] = b'PSEQ'
        struct.pack_into('<HBBHIIB', header, 4, 32, 0, 2, 32, 48, self.frames, 20)
        self.path.write_bytes(header + self.data)

    def put(self, channel, start, end, value=255):
        for i in range(start, end):
            self.data[i*48+channel-1] = value

    def musical(self):
        for c in [13, 14, 23, 24]:
            for i in range(8):
                self.put(c, i*50+10, i*50+20)
        self.put(7, 500, 530, 178)
        self.put(8, 550, 580, 178)
        self.put(11, 600, 710, 229)
        self.write()

    def test_valid_musical(self):
        self.musical()
        self.assertEqual(validate(self.path, musical=True)['channels'][13]['onsets'], 8)

    def test_missing_front_amber_regression(self):
        self.musical()
        self.put(13, 0, self.frames, 0)
        self.write()
        with self.assertRaisesRegex(ValueError, '13 inactive'):
            validate(self.path, musical=True)

    def test_mechanical_rejected(self):
        self.put(41, 10, 20)
        self.write()
        with self.assertRaisesRegex(ValueError, 'Mechanical'):
            validate(self.path)

    def test_truncated_payload(self):
        self.write()
        self.path.write_bytes(self.path.read_bytes()[:-1])
        with self.assertRaisesRegex(ValueError, 'Payload'):
            validate(self.path)

    def test_final_blackout(self):
        self.put(11, 998, 1000)
        self.write()
        with self.assertRaisesRegex(ValueError, 'dark'):
            validate(self.path)

    def test_short_amber_pulse(self):
        self.musical()
        self.put(13, 10, 20, 0)
        self.put(13, 10, 12)
        self.write()
        with self.assertRaisesRegex(ValueError, 'shorter'):
            validate(self.path, musical=True)

    def test_duplicate_center_rejected_in_music(self):
        self.musical()
        self.put(12, 600, 700)
        self.write()
        with self.assertRaisesRegex(ValueError, '12 outside'):
            validate(self.path, musical=True)

    def test_white_amber_conflict(self):
        self.musical()
        self.put(7, 10, 20)
        self.write()
        with self.assertRaisesRegex(ValueError, 'overlap'):
            validate(self.path, musical=True)

    def test_probe_and_no_overwrite(self):
        folder = Path(self.temp.name) / 'probe'
        with contextlib.redirect_stdout(io.StringIO()):
            build(folder)
        show = folder / 'LightShow/juniper_fade_probe'
        report = validate(show.with_suffix('.fseq'), show.with_suffix('.wav'))
        self.assertEqual(report['duration_seconds'], 51)
        self.assertGreater(report['channels'][12]['onsets'], 0)
        with self.assertRaises(FileExistsError):
            build(folder)


if __name__ == '__main__':
    unittest.main()
