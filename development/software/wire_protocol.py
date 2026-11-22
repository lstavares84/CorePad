"""Byte framing for the public configuration channel; transport independent.

No biometric, third-layer or secret command exists on this channel. CRC detects
accidental corruption; it does not authenticate the host or encrypt traffic.
"""
import json
import struct
import zlib
from device import Simulator

MAGIC = b"CPD1"
VERSION = 1
GET_CONFIG = 1
SET_CONFIG = 2
ACK = 0x82
CONFIG = 0x81
MAX_PAYLOAD = 32768
HEADER = struct.Struct("<4sBBHH")
CRC = struct.Struct("<I")


def encode(opcode, request_id, payload=b""):
    if opcode not in (GET_CONFIG, SET_CONFIG, ACK, CONFIG):
        raise ValueError("opcode publico desconhecido")
    if not 0 <= request_id <= 65535 or len(payload) > MAX_PAYLOAD:
        raise ValueError("ID ou comprimento invalido")
    header = HEADER.pack(MAGIC, VERSION, opcode, request_id, len(payload))
    body = header + payload
    return body + CRC.pack(zlib.crc32(body))


def decode(frame):
    if len(frame) < HEADER.size + CRC.size:
        raise ValueError("quadro incompleto")
    magic, version, opcode, request_id, size = HEADER.unpack_from(frame)
    if magic != MAGIC or version != VERSION or opcode not in (GET_CONFIG, SET_CONFIG, ACK, CONFIG):
        raise ValueError("cabecalho invalido")
    if size > MAX_PAYLOAD or len(frame) != HEADER.size + size + CRC.size:
        raise ValueError("comprimento invalido")
    expected, = CRC.unpack_from(frame, HEADER.size + size)
    if zlib.crc32(frame[:-CRC.size]) != expected:
        raise ValueError("CRC invalido")
    return opcode, request_id, frame[HEADER.size:-CRC.size]


def json_payload(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def simulator_exchange(simulator: Simulator, frame: bytes):
    opcode, request_id, payload = decode(frame)
    if opcode == GET_CONFIG:
        if payload:
            raise ValueError("GET sem payload")
        return encode(CONFIG, request_id, json_payload(simulator.request({"command": "get_config"})))
    if opcode == SET_CONFIG:
        config = json.loads(payload.decode("utf-8"))
        simulator.request({"command": "set_config", "config": config})
        return encode(ACK, request_id, b"")
    raise ValueError("resposta nao e comando")
