"""ATDA HW-01 synthetic sensor framing contract.

STRICTLY A SOFTWARE UNIT-TEST REFERENCE. This does not remove PII in hardware,
provide replay protection, certify isolation or implement Path A alarm logic.
Internal lab sensor -> acquisition boundary only; never connect to live payment.
"""
from __future__ import annotations
from dataclasses import dataclass

FRAME_VERSION = 1
CLASS_NAMES = ("MAINTENANCE", "NARCOTICS", "BIOHAZARD", "OTHER")
FRAME_LENGTH = 4

class FrameRejected(ValueError):
    """An internal sensor frame is malformed or outside the frozen contract."""

@dataclass(frozen=True)
class Observation:
    class_name: str
    quality_valid: bool

def crc8(data: bytes) -> int:
    """CRC-8 poly=0x07 init=0; checks transport errors, NOT authenticity."""
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc << 1) ^ 0x07) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
    return crc

def decode_lab_frame(frame: bytes) -> Observation:
    """Accept only a 4-byte version/class/quality/CRC message.

    No variable fields, IDs, per-event timestamps, or raw payload are present.
    Timing correlation remains a residual privacy risk; independent hardware
    verification and a downstream hard k-gate are still mandatory.
    """
    if type(frame) is not bytes or len(frame) != FRAME_LENGTH:
        raise FrameRejected("INVALID_FRAME_LENGTH_OR_TYPE")
    version, class_code, quality, check = frame
    if version != FRAME_VERSION:
        raise FrameRejected("UNRECOGNISED_VERSION")
    if class_code >= len(CLASS_NAMES):
        raise FrameRejected("INVALID_CLASS")
    if quality not in (0, 1):
        raise FrameRejected("RESERVED_QUALITY_BITS")
    if crc8(frame[:3]) != check:
        raise FrameRejected("CRC_ERROR")
    return Observation(class_name=CLASS_NAMES[class_code], quality_valid=bool(quality))

def make_synthetic_frame(class_code: int, valid: bool = True) -> bytes:
    """Test fixture helper only; no production input or secrets."""
    if type(class_code) is not int or class_code not in range(len(CLASS_NAMES)):
        raise FrameRejected("INVALID_CLASS")
    if type(valid) is not bool:
        raise FrameRejected("INVALID_QUALITY")
    body = bytes((FRAME_VERSION, class_code, int(valid)))
    return body + bytes((crc8(body),))
