# Mesin Absensi dengan Sensor AS608 dan ESP8266

## Deskripsi Proyek
Proyek ini merupakan sistem absensi berbasis IoT yang menggunakan sensor sidik jari AS608, RTC, dan ESP8266 untuk mencatat kehadiran siswa. Data absensi dikirim ke platform **Ubidots** untuk monitoring dan ke database. Sistem ini juga terintegrasi dengan **chatbot berbasis AI** untuk menjawab pertanyaan seputar status kehadiran siswa secara interaktif, dan **dashboard visualisasi di Streamlit** untuk analisis data secara real-time.

## Teknologi yang Digunakan
### Hardware
- **Sensor Sidik Jari AS608** – untuk identifikasi biometrik.
- **RTC (Real-Time Clock)** – untuk mencatat waktu absensi.
- **ESP8266** – sebagai mikrokontroler dan penghubung ke internet.
- **Tombol (Button)** – untuk input manual jika diperlukan.

### Software & Tools
- **Ubidots** – platform IoT untuk pengiriman dan visualisasi data.
- **Streamlit** – untuk membuat dashboard visualisasi absensi secara real-time.
- **MongoDB / Firebase / File Cloud** – sebagai penyimpanan data absensi.
- **Chatbot AI (misalnya ChatGPT / Rasa / Dialogflow)** – untuk menjawab pertanyaan seperti “Siapa saja yang terlambat hari ini?” atau “Berapa persen kehadiran minggu ini?”
- **Thonny** – IDE Python untuk pemrograman ESP8266.

## Fitur Utama
✅ **Pengenalan Sidik Jari** dengan sensor AS608  
✅ **Pencatatan Waktu Otomatis** menggunakan RTC  
✅ **Koneksi Internet** melalui ESP8266  
✅ **Pengiriman & Visualisasi Data** ke Ubidots  
✅ **Chatbot Interaktif** untuk tanya jawab kehadiran  
✅ **Dashboard di Streamlit** untuk analisis visual kehadiran  
✅ **Status Kehadiran Otomatis** berdasarkan waktu  
✅ **Notifikasi Keterlambatan** berbasis AI

## Struktur Data
Contoh data absensi yang dikirim:
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
- Tempelkan jari pada sensor AS608 untuk mendaftarkan sidik jari.
- Data sidik jari disimpan di memori ESP8266.

### 2. Proses Absensi
- Tempelkan jari untuk verifikasi.
- Jika cocok, data waktu kehadiran dikirim ke **Ubidots**.

### 3. Analisis dan Interaksi
- **Dashboard Streamlit** menampilkan grafik dan statistik kehadiran siswa.
- **Chatbot AI** menjawab pertanyaan seperti:
  - “Siapa saja yang tidak hadir hari ini?”
  - “Apakah siswa X sering terlambat?”

## Instalasi & Konfigurasi
1. **Siapkan Perangkat Keras**
   - Hubungkan sensor AS608, RTC, dan tombol ke ESP8266.

2. **Konfigurasi Platform**
   - Buat akun di **Ubidots** dan siapkan dashboard.
   - Siapkan **Streamlit app** dan integrasikan dengan database.
   - Deploy **chatbot AI** (gunakan webhook jika ingin chatbot merespons data absensi dari server).

3. **Instalasi Software**
   - Install pustaka Python:
     ```bash
     pip install streamlit pymongo requests
     ```

4. **Jalankan Program**
   - Unggah kode ke ESP8266 via Thonny.
   - Jalankan Streamlit dan chatbot AI.

## Pengembangan Selanjutnya
🚀 **Integrasi Mobile App** untuk siswa dan orang tua  
💬 **Notifikasi WhatsApp / Telegram** dari chatbot  
📈 **Prediksi Pola Kehadiran** menggunakan Machine Learning  
📅 **Fitur Kalender Absensi** di dashboard

## Kontributor
- **[Dwi Nur Cahya](https://github.com/dwincahya)**
- **[Juandito Yefta Priatama](https://github.com/juanditoyeftapriatama)**
- **[Emilliano Sebastian Freitas](https://github.com/SoramiKS)**
- **[Oreo Majhesta](https://github.com/OreoMajhesta)**
