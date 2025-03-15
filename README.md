# Mesin Absensi dengan Sensor AS608 dan ESP8266

## Deskripsi Proyek
Proyek ini merupakan sistem absensi berbasis IoT yang menggunakan sensor sidik jari AS608, RTC, dan ESP8266 untuk mencatat kehadiran siswa. Data absensi dikirim ke database MongoDB melalui Ubidots, serta dianalisis menggunakan model AI berbasis CNN. Sistem ini dapat mendeteksi apakah siswa terlambat atau hadir tepat waktu berdasarkan waktu yang tercatat.

## Teknologi yang Digunakan
- **Hardware:**
  - Sensor Sidik Jari AS608
  - RTC (Real-Time Clock)
  - ESP8266
  - Tombol (Button)
- **Software & Tools:**
  - Ubidots (IoT Platform)
  - MongoDB (Database)
  - Thonny (Python IDE)
  - CNN (Convolutional Neural Network) untuk analisis AI

## Fitur
- **Pengenalan Sidik Jari** dengan sensor AS608
- **Pencatatan Waktu** menggunakan RTC
- **Koneksi Internet** melalui ESP8266
- **Penyimpanan Data** ke MongoDB melalui Ubidots
- **Analisis AI** untuk memprediksi keterlambatan
- **Status Kehadiran** (Hadir/Terlambat) berdasarkan waktu absen

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
1. **Pendaftaran Sidik Jari**
   - Tempelkan jari pada sensor AS608 untuk mendaftarkan sidik jari pertama kali.
   - Data sidik jari akan disimpan di ESP8266.
2. **Proses Absensi**
   - Tempelkan jari pada sensor untuk verifikasi.
   - Jika cocok, sistem akan mencatat waktu dan mengirim data ke MongoDB melalui Ubidots.
3. **Analisis Kehadiran**
   - Model AI berbasis CNN akan memproses data untuk menentukan status keterlambatan.
   
## Instalasi
1. **Persiapkan Perangkat Keras**
   - Hubungkan sensor AS608, RTC, dan tombol ke ESP8266 sesuai skema yang telah dibuat.
2. **Konfigurasi Perangkat Lunak**
   - Pastikan memiliki akun Ubidots dan MongoDB.
   - Install pustaka yang diperlukan di Thonny:
     ```bash
     pip install pymongo requests
     ```
3. **Jalankan Program**
   - Unggah kode ke ESP8266 dan jalankan skrip Python di Thonny.

## Pengembangan Selanjutnya
- Integrasi dengan aplikasi mobile untuk akses data absensi secara real-time.
- Peningkatan akurasi AI untuk prediksi keterlambatan.

## Kontributor
- **Nama Anda** - Pengembang Utama

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
