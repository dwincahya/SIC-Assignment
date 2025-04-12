from machine import UART, Pin, I2C
from time import sleep
from as608_combo_lib import AS608
from utils import simpan_nama, get_nama, load_nama
import ds3231
import os

# Inisialisasi
uart = UART(2, baudrate=57600, tx=17, rx=16, timeout=2000)
sensor = AS608(uart)
btn_enroll = Pin(4, Pin.IN, Pin.PULL_UP)
btn_match = Pin(5, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
rtc = ds3231.DS3231(i2c)

# Log hadir harian (format: {ID: True})
absen_hari_ini = {}

def format_waktu(waktu_tuple):
    y, m, d, wd, h, mi, s = waktu_tuple
    return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d}"

def cek_status_kehadiran(waktu):
    _, _, _, _, h, mi, s = waktu
    if h < 6 or (h == 6 and mi <= 45):
        return "Hadir"
    return "Terlambat"

def log_absen(nama, waktu_str, status):
    baris = f"{waktu_str} - {nama} - {status}\n"
    try:
        with open("absen_log.txt", "a") as f:
            f.write(baris)
    except:
        print("Gagal menyimpan log.")

def cari_sidik_jari():
    print("Letakkan jari untuk pencocokan...")
    while not sensor.capture_image():
        pass
    if not sensor.image2Tz(1):
        print("Gagal membaca gambar.")
        return
    result = sensor.search()
    if result:
        ID = result['id']
        if ID in absen_hari_ini:
            print("ID ini sudah absen hari ini.")
            return
        nama = get_nama(ID)
        waktu = rtc.datetime()
        waktu_str = format_waktu(waktu)
        status = cek_status_kehadiran(waktu)
        log_absen(nama, waktu_str, status)
        absen_hari_ini[ID] = True
        print(f"{nama} masuk pada {waktu_str} ({status})")
    else:
        print("Sidik jari tidak dikenali.")

def daftar_sidik_jari():
    try:
        ID = int(input("Masukkan ID untuk sidik jari (0-255): "))
        if not (0 <= ID <= 255):
            print("ID harus antara 0 sampai 255.")
            return
    except:
        print("ID tidak valid.")
        return

    nama = input("Masukkan nama untuk ID ini: ")
    if not nama:
        print("Nama tidak boleh kosong.")
        return

    print("Letakkan jari di sensor...")
    while not sensor.capture_image():
        pass
    if not sensor.image2Tz(1):
        print("Gagal mengkonversi gambar.")
        return
    print("Angkat jari dan letakkan kembali...")
    sleep(2)
    while not sensor.capture_image():
        pass
    if not sensor.image2Tz(2):
        print("Gagal gambar kedua.")
        return
    if sensor.create_model() and sensor.store_model(ID):
        simpan_nama(ID, nama)
        print(f"Sidik jari '{nama}' berhasil didaftarkan.")
    else:
        print("Pendaftaran gagal.")

def cek_absen_sore():
    waktu = rtc.datetime()
    if waktu[4] == 14 and waktu[5] == 0:  # Jam 14:00
        semua = load_nama()
        for id_str, nama in semua.items():
            if int(id_str) not in absen_hari_ini:
                waktu_str = format_waktu(waktu)
                log_absen(nama, waktu_str, "Tidak Masuk")
                print(f"{nama} tidak masuk (absen jam 14.00)")

# Cek sensor
print("Menginisialisasi sensor fingerprint...")
if sensor.handshake():
    print("Sensor fingerprint terdeteksi!")
    sensor.set_led(True)
else:
    print("Gagal mendeteksi sensor fingerprint.")

# Loop utama
while True:
    if not btn_enroll.value():
        print("Mode: Pendaftaran Sidik Jari")
        daftar_sidik_jari()
        sleep(1)

    if not btn_match.value():
        print("Mode: Pencocokan Sidik Jari")
        cari_sidik_jari()
        sleep(1)

    cek_absen_sore()
    sleep(1)
