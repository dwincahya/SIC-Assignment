from machine import UART, Pin, I2C
from time import sleep
from as608_combo_lib import AS608
from utils import simpan_nama, get_nama, load_nama
import ds3231
import os
import network
import urequests

# === Konfigurasi WiFi dan API ===
SSID = "YEFTA"
PASSWORD = "085705652088"
API_URL = "http://192.168.1.2:5000/api/absen"

# === Inisialisasi Perangkat ===
uart = UART(2, baudrate=57600, tx=17, rx=16, timeout=2000)
sensor = AS608(uart)
btn_enroll = Pin(4, Pin.IN, Pin.PULL_UP)
btn_match = Pin(5, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
rtc = ds3231.DS3231(i2c)
absen_hari_ini = {}

# === Fungsi Koneksi WiFi ===
def konek_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            sleep(1)
    print("Terhubung ke WiFi:", wlan.ifconfig())

# === Format Waktu ===
def format_waktu(waktu_tuple):
    y, m, d, wd, h, mi, s = waktu_tuple
    return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d}"

# === Cek Status Kehadiran ===
def cek_status_kehadiran(waktu):
    _, _, _, _, h, mi, _ = waktu
    if h < 6 or (h == 6 and mi <= 45):
        return "Hadir"
    return "Terlambat"

# === Simpan Log ke File Lokal ===
def log_absen(nama, waktu_str, status):
    baris = f"{waktu_str} - {nama} - {status}\n"
    try:
        with open("absen_log.txt", "a") as f:
            f.write(baris)
    except:
        print("Gagal menyimpan log lokal.")

# === Kirim Data ke MongoDB via Flask ===
def kirim_ke_api(nama, waktu_iso, status, ID, kelas="SIJA 2"):
    data = {
        "id": ID,
        "nama": nama,
        "kelas": kelas,
        "no_presensi": ID,
        "waktu": waktu_iso + "Z",
        "status": status
    }
    try:
        res = urequests.post(API_URL, json=data)
        print("Terkirim ke server:", res.text)
        res.close()
    except Exception as e:
        print("Gagal kirim ke server:", e)

# === Fungsi Absen (Pencocokan Sidik Jari) ===
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
        info = get_nama(ID)
        nama = info["nama"]
        kelas = info["kelas"]
        waktu = rtc.datetime()
        waktu_str = format_waktu(waktu)
        status = cek_status_kehadiran(waktu)
        log_absen(nama, waktu_str, status)
        waktu_iso = waktu_str.replace(" ", "T")
        kirim_ke_api(nama, waktu_iso, status, ID, kelas)
        absen_hari_ini[ID] = True
        print(f"{nama} masuk pada {waktu_str} ({status})")
    else:
        print("Sidik jari tidak dikenali.")

# === Fungsi Daftar Sidik Jari Baru ===
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
    kelas = input("Masukkan kelas untuk ID ini: ")

    if not nama or not kelas:
        print("Nama dan kelas tidak boleh kosong.")
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
        simpan_nama(ID, nama, kelas)
        print(f"Sidik jari '{nama}' dari kelas '{kelas}' berhasil didaftarkan.")
    else:
        print("Pendaftaran gagal.")

# === Fungsi Cek Sore (14:00) saat looping ===
def cek_absen_sore():
    waktu = rtc.datetime()
    if waktu[4] == 14 and waktu[5] == 0:
        semua = load_nama()
        for id_str, info in semua.items():
            ID = int(id_str)
            if ID not in absen_hari_ini:
                waktu_str = format_waktu(waktu)
                log_absen(info["nama"], waktu_str, "Tidak Hadir")
                waktu_iso = waktu_str.replace(" ", "T")
                kirim_ke_api(info["nama"], waktu_iso, "Tidak Hadir", ID, info["kelas"])
                print(f"{info['nama']} tidak Hadir (absen jam 14.00)")

# === Fungsi Cek Terlambat Saat Boot ===
def cek_absen_terlewat_saat_boot():
    waktu = rtc.datetime()
    if waktu[4] > 14 or (waktu[4] == 14 and waktu[5] > 0):
        semua = load_nama()
        try:
            with open("absen_log.txt", "r") as f:
                log = f.readlines()
        except:
            log = []

        hari_ini = f"{waktu[0]:04d}-{waktu[1]:02d}-{waktu[2]:02d}"
        sudah_absen = set()
        for baris in log:
            if hari_ini in baris:
                for id_str, info in semua.items():
                    if info["nama"] in baris:
                        sudah_absen.add(int(id_str))

        for id_str, info in semua.items():
            ID = int(id_str)
            if ID not in sudah_absen:
                waktu_str = format_waktu(waktu)
                log_absen(info["nama"], waktu_str, "Tidak Masuk")
                waktu_iso = waktu_str.replace(" ", "T")
                kirim_ke_api(info["nama"], waktu_iso, "Tidak Masuk", ID, info["kelas"])
                print(f"{info['nama']} dari kelas {info['kelas']} dinyatakan Tidak Masuk (terlambat cek)")
                absen_hari_ini[ID] = True

# === MAIN ===
print("Menginisialisasi sensor fingerprint...")
konek_wifi()
cek_absen_terlewat_saat_boot()  # ⏱ Cek saat boot

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
