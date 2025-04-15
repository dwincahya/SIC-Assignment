# Mesin Absensi dengan Sensor AS608 dan ESP32

## Deskripsi Proyek
Proyek ini merupakan sistem absensi berbasis IoT yang menggunakan sensor sidik jari AS608, RTC, dan **ESP32** untuk mencatat kehadiran siswa. Data absensi dikirim ke platform **Ubidots** untuk monitoring dan juga disimpan ke **MongoDB**. Sistem ini terintegrasi dengan **asisten AI berbasis Gemini** dari Google, yang tertanam dalam **dashboard Streamlit**, memungkinkan interaksi langsung dengan guru untuk menanyakan status kehadiran siswa secara real-time.

## Teknologi yang Digunakan
### Hardware
- **Sensor Sidik Jari AS608** – untuk identifikasi biometrik.
- **RTC (Real-Time Clock)** – untuk mencatat waktu absensi.
- **ESP32** – sebagai mikrokontroler dengan konektivitas Wi-Fi.
- **2 Tombol (Push Button)**:
  - Tombol 1: untuk masuk ke mode pendaftaran sidik jari.
  - Tombol 2: untuk proses absensi (verifikasi sidik jari siswa).

### Software & Tools
- **Ubidots** – platform IoT untuk pengiriman dan visualisasi data.
- **Streamlit** – untuk membuat dashboard visualisasi absensi secara real-time.
- **MongoDB** – sebagai basis data utama untuk menyimpan catatan absensi.
- **Gemini AI (via API Google AI)** – chatbot yang terintegrasi di dalam Streamlit.
- **Thonny / Arduino IDE** – untuk pemrograman ESP32.

## Fitur Utama
✅ **Pengenalan Sidik Jari** dengan sensor AS608  
✅ **Pencatatan Waktu Otomatis** menggunakan RTC  
✅ **ESP32 sebagai Otak Sistem** dengan konektivitas ke Wi-Fi  
✅ **Pengiriman Data ke Ubidots** untuk monitoring  
✅ **Penyimpanan Data di MongoDB** untuk histori lengkap  
✅ **Dashboard Streamlit** yang intuitif dan interaktif  
✅ **Gemini AI Chatbot** untuk tanya jawab tentang data kehadiran  
✅ **Notifikasi dan Insight** berbasis data real-time  

## Struktur Data
Contoh data absensi:
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
### 1. Mode Pendaftaran Sidik Jari
- Tekan **Tombol 1** untuk masuk ke mode pendaftaran.
- Tempelkan jari pada sensor AS608.
- Data sidik jari disimpan di memori ESP32.

### 2. Mode Absensi
- Tekan **Tombol 2** untuk mulai mode absensi.
- Tempelkan jari untuk verifikasi.
- Jika cocok, data waktu kehadiran dikirim ke **Ubidots** dan **MongoDB**.

### 3. Dashboard dan Chatbot
- Buka dashboard Streamlit.
- Lihat grafik kehadiran dan statistik per kelas/per siswa.
- Gunakan **Gemini chatbot** untuk bertanya:
  - “Siapa saja yang tidak hadir hari ini?”
  - “Berapa persen kehadiran minggu ini?”
  - “Apakah siswa X sering terlambat?”

## Instalasi & Konfigurasi
1. **Siapkan Hardware**
   - Hubungkan sensor AS608, RTC, dan dua tombol ke ESP32.

2. **Siapkan Platform**
   - Daftar dan buat dashboard di **Ubidots**.
   - Siapkan database **MongoDB (Atlas)**.
   - Buat aplikasi **Streamlit** dan integrasikan Gemini API.

3. **Install Software**
   - Install pustaka Python:
     ```bash
     pip install streamlit pymongo requests google-generativeai
     ```

4. **Jalankan Sistem**
   - Upload firmware ke ESP32 (via Thonny/Arduino IDE).
   - Jalankan aplikasi Streamlit:
     ```bash
     streamlit run chat.py
     ```

## Pengembangan Selanjutnya
💬 **Notifikasi WhatsApp / Telegram**
📊 **Analisis Prediktif** dengan Machine Learning  

## Kontributor
- **[Dwi Nur Cahya](https://github.com/dwincahya)**
- **[Juandito Yefta Priatama](https://github.com/juanditoyeftapriatama)**
- **[Emilliano Sebastian Freitas](https://github.com/SoramiKS)**
- **[Oreo Majhesta](https://github.com/OreoMajhesta)**

