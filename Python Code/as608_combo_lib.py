import struct
import time

class AS608:
    def __init__(self, uart):
        self.uart = uart
        self.address = b'\xFF\xFF\xFF\xFF'
        self.password = b'\x00\x00\x00\x00'

    def _send_packet(self, packet_type, payload):
        length = len(payload) + 2
        packet = b'\xEF\x01' + self.address
        packet += struct.pack('>B', packet_type)
        packet += struct.pack('>H', length)
        packet += payload
        checksum = packet_type + length + sum(payload)
        packet += struct.pack('>H', checksum)
        self.uart.write(packet)

    def _read_packet(self, timeout=2000):
        start = time.ticks_ms()
        while self.uart.any() < 9:
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                return None
        header = self.uart.read(9)
        if not header or len(header) < 9:
            return None
        pkt_type = header[6]
        pkt_len = struct.unpack('>H', header[7:9])[0]
        data = self.uart.read(pkt_len)
        return data[:-2] if data and len(data) >= pkt_len else None

    def handshake(self):
        self._send_packet(0x01, b'\x17')
        resp = self._read_packet()
        return resp and resp[0] == 0x00

    def set_led(self, on=True):
        self._send_packet(0x01, b'\x35\x01' + (b'\x01' if on else b'\x00'))
        resp = self._read_packet()
        return resp and resp[0] == 0x00

    def capture_image(self):
        self._send_packet(0x01, b'\x01')
        resp = self._read_packet()
        return resp and resp[0] == 0x00

    def image2Tz(self, buffer_id=1):
        self._send_packet(0x01, b'\x02' + bytes([buffer_id]))
        resp = self._read_packet()
        return resp and resp[0] == 0x00

    def create_model(self):
        self._send_packet(0x01, b'\x05')
        resp = self._read_packet()
        return resp and resp[0] == 0x00

    def store_model(self, page_id):
        pid_high = (page_id >> 8) & 0xFF
        pid_low = page_id & 0xFF
        self._send_packet(0x01, b'\x06\x01' + bytes([pid_high, pid_low]))
        resp = self._read_packet()
        return resp and resp[0] == 0x00

    def search(self):
        self._send_packet(0x01, b'\x04\x01\x00\x00\x00\xA3')  # Search from ID 0 to 0x00A3 (163)
        resp = self._read_packet()
        if resp and resp[0] == 0x00:
            match_id = (resp[1] << 8) | resp[2]
            score = (resp[3] << 8) | resp[4]
            return {'id': match_id, 'score': score}
        return None
