"""HW-01 contract tests are software tests, NEVER evidence of a physical diode."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hw01_boundary_contract import (
    CLASS_NAMES, FrameRejected, crc8, decode_lab_frame, make_synthetic_frame
)

class HardwareBoundaryContractTests(unittest.TestCase):
    def test_roundtrip_all_classes(self):
        for i, name in enumerate(CLASS_NAMES):
            self.assertEqual(decode_lab_frame(make_synthetic_frame(i)).class_name, name)
    def test_maintenance_is_not_security_alert(self):
        self.assertEqual(decode_lab_frame(make_synthetic_frame(0)).class_name, "MAINTENANCE")
    def test_invalid_quality_can_be_represented(self):
        self.assertFalse(decode_lab_frame(make_synthetic_frame(2, False)).quality_valid)
    def test_frame_is_constant_length(self):
        self.assertTrue(all(len(make_synthetic_frame(i)) == 4 for i in range(4)))
    def test_no_extra_payload(self):
        with self.assertRaises(FrameRejected):
            decode_lab_frame(make_synthetic_frame(1) + b"payment_ID")
    def test_no_short_frame(self):
        with self.assertRaises(FrameRejected):
            decode_lab_frame(make_synthetic_frame(1)[:3])
    def test_wrong_version(self):
        x = bytearray(make_synthetic_frame(1)); x[0] = 2
        x[3] = crc8(x[:3])
        with self.assertRaises(FrameRejected):
            decode_lab_frame(bytes(x))
    def test_out_of_range_class(self):
        x = bytearray(make_synthetic_frame(1)); x[1] = 255
        x[3] = crc8(x[:3])
        with self.assertRaises(FrameRejected):
            decode_lab_frame(bytes(x))
    def test_bad_crc(self):
        x = bytearray(make_synthetic_frame(1)); x[3] ^= 1
        with self.assertRaises(FrameRejected):
            decode_lab_frame(bytes(x))
    def test_reserved_quality_bit(self):
        x = bytearray(make_synthetic_frame(1)); x[2] = 2
        x[3] = crc8(x[:3])
        with self.assertRaises(FrameRejected):
            decode_lab_frame(bytes(x))
    def test_reject_bytearray(self):
        with self.assertRaises(FrameRejected):
            decode_lab_frame(bytearray(make_synthetic_frame(1)))
    def test_reject_string(self):
        with self.assertRaises(FrameRejected):
            decode_lab_frame("test")
    def test_reject_bad_fixture_class(self):
        with self.assertRaises(FrameRejected):
            make_synthetic_frame(-1)
    def test_reject_bool_as_class(self):
        with self.assertRaises(FrameRejected):
            make_synthetic_frame(True)
    def test_reject_invalid_fixture_quality(self):
        with self.assertRaises(FrameRejected):
            make_synthetic_frame(1, 1)

if __name__ == "__main__":
    unittest.main()
