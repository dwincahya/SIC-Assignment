# Mesin Absensi dengan Sensor AS608 dan ESP8266

## Deskripsi Proyek
Proyek ini merupakan sistem absensi berbasis IoT yang menggunakan sensor sidik jari AS608, RTC, dan ESP8266 untuk mencatat kehadiran siswa. Data absensi dikirim ke database MongoDB melalui Ubidots, serta dianalisis menggunakan model AI berbasis CNN. Sistem ini dapat mendeteksi apakah siswa terlambat atau hadir tepat waktu berdasarkan waktu yang tercatat.

## Teknologi yang Digunakan
### Hardware
- **Sensor Sidik Jari AS608** – untuk identifikasi biometrik.
- **RTC (Real-Time Clock)** – untuk mencatat waktu absensi.
- **ESP8266** – sebagai mikrokontroler dan penghubung ke internet.
- **Tombol (Button)** – untuk input manual jika diperlukan.

### Software & Tools
- **Ubidots** – platform IoT untuk pengiriman data.
- **MongoDB** – database untuk menyimpan data absensi.
- **Thonny** – IDE Python untuk pemrograman ESP8266.
- **CNN (Convolutional Neural Network)** – untuk analisis AI dalam menentukan status keterlambatan.

## Fitur Utama
✅ **Pengenalan Sidik Jari** dengan sensor AS608
✅ **Pencatatan Waktu Otomatis** menggunakan RTC
✅ **Koneksi ke Internet** melalui ESP8266
✅ **Penyimpanan Data Cloud** dengan MongoDB melalui Ubidots
✅ **Analisis AI** untuk memprediksi keterlambatan
✅ **Status Kehadiran** (Hadir/Terlambat) secara otomatis
✅ **Dashboard Visualisasi** untuk memantau data absensi

## Struktur Data
Data yang dikirim ke database memiliki format berikut:
```json
{
  "id": "123456",
  "nama": "John Doe",
  "kelas": "XII IPA 1",
  "waktu": "2025-03-15T08:30:00Z",
  "status": "Hadir"
}
```

## Cara Menggunakan
### 1. Pendaftaran Sidik Jari
- Tempelkan jari pada sensor AS608 untuk mendaftarkan sidik jari pertama kali.
- Data sidik jari akan disimpan di ESP8266.

### 2. Proses Absensi
- Tempelkan jari pada sensor untuk verifikasi.
- Jika cocok, sistem akan mencatat waktu dan mengirim data ke MongoDB melalui Ubidots.

### 3. Analisis Kehadiran
- Model AI berbasis CNN akan memproses data untuk menentukan status keterlambatan.
- Data dapat diakses melalui dashboard untuk monitoring real-time.

## Instalasi & Konfigurasi
1. **Siapkan Perangkat Keras**
   - Hubungkan sensor AS608, RTC, dan tombol ke ESP8266 sesuai skema rangkaian.
2. **Konfigurasi Software**
   - Buat akun di **Ubidots** dan **MongoDB**.
   - Install pustaka Python yang dibutuhkan:
     ```bash
     pip install pymongo requests
     ```
3. **Jalankan Program**
   - Unggah kode ke ESP8266.
   - Jalankan skrip Python di Thonny untuk menghubungkan perangkat.

## Pengembangan Selanjutnya
🚀 **Integrasi dengan aplikasi mobile** untuk akses data secara real-time.
📊 **Peningkatan AI** agar lebih akurat dalam menganalisis keterlambatan.
🔗 **Notifikasi otomatis** ke siswa/guru jika ada keterlambatan.

## Kontributor
- **[Dwi Nur Cahya](https://github.com/dwincahya)**
- **[Juandito Yefta Priatama](https://github.com/juanditoyeftapriatama)**
- **[Emilliano Sebastian Freitas](https://github.com/SoramiKS)**
- **[Oreo Majhesta](https://github.com/OreoMajhesta)**
