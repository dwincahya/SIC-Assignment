# ds3231.py
class DS3231:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 104

    def _bcd2dec(self, bcd): return (bcd // 16) * 10 + (bcd % 16)
    def _dec2bcd(self, dec): return (dec // 10) * 16 + (dec % 10)

    def datetime(self):
        data = self.i2c.readfrom_mem(self.addr, 0x00, 7)
        ss = self._bcd2dec(data[0])
        mm = self._bcd2dec(data[1])
        hh = self._bcd2dec(data[2])
        wd = self._bcd2dec(data[3])
        dd = self._bcd2dec(data[4])
        mo = self._bcd2dec(data[5])
        yy = self._bcd2dec(data[6]) + 2000
        return (yy, mo, dd, wd, hh, mm, ss)

    def set_datetime(self, dt):
        yy, mo, dd, wd, hh, mm, ss = dt
        data = bytes([
            self._dec2bcd(ss),
            self._dec2bcd(mm),
            self._dec2bcd(hh),
            self._dec2bcd(wd),
            self._dec2bcd(dd),
            self._dec2bcd(mo),
            self._dec2bcd(yy - 2000)
        ])
        self.i2c.writeto_mem(self.addr, 0x00, data)
