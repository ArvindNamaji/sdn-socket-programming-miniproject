import struct
import zlib

HEADER_FORMAT = "!IIHH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

FLAG_DATA = 1
FLAG_ACK  = 2
FLAG_FIN  = 4

def calculate_checksum(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFF

def make_packet(seq_num: int, ack_num: int, flags: int, payload: bytes = b"") -> bytes:
    checksum = calculate_checksum(payload)
    header = struct.pack(HEADER_FORMAT, seq_num, ack_num, flags, checksum)
    return header + payload

def parse_packet(raw_bytes: bytes):
    if len(raw_bytes) < HEADER_SIZE:
        return None
    seq_num, ack_num, flags, checksum = struct.unpack(HEADER_FORMAT, raw_bytes[:HEADER_SIZE])
    payload = raw_bytes[HEADER_SIZE:]
    is_valid = (calculate_checksum(payload) == checksum)
    return {
        "seq_num": seq_num,
        "ack_num": ack_num,
        "flags": flags,
        "checksum": checksum,
        "payload": payload,
        "is_valid": is_valid
    }
