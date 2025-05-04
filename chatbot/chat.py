import streamlit as st
from pymongo import MongoClient
from google.generativeai import GenerativeModel, configure
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from datetime import timezone
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

st.title("TouchTrace")


# Konfigurasi Gemini API
configure(api_key=os.getenv("GEMINI_API"))
gemini = GenerativeModel("models/gemini-1.5-pro")

# Koneksi MongoDB
client = MongoClient("mongodb+srv://juanditoyeftapriatama:jyp120707@cluster0.rmdy1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["sekolah"]
collection = db["kehadiran"]

menu = st.sidebar.radio("Pilih tampilan", ["Chatbot", "Chart Absensi"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# =================== CHATBOT ===================
if menu == "Chatbot":
    # UI
    st.header("🤖 Chatbot Absensi Siswa (Gemini)", divider="gray")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Tanyakan sesuatu...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        data = list(collection.find())

        absensi_list = ""
        for d in data:
            absensi_list += f"{d.get('nama', 'Tidak diketahui')} ({d.get('kelas', '-')}) - {d.get('status', '-')}, {d.get('waktu', '-')}\n"

        prompt = f"""
        Kamu adalah asisten AI lucu dan asik yang menjawab pertanyaan tentang absensi siswa berdasarkan data berikut:

        {absensi_list}

        Pertanyaan: {user_input}
        Jawablah berdasarkan data absensi di atas dan rapi.
        Jika jawaban tidak terkait dengan absensi, jawab seperti biasa dan tidak usah perdulikan data nya.
        """

        with st.chat_message("assistant"):
            msg = st.empty()
            response = ""
            for chunk in gemini.generate_content(prompt, stream=True):
                response += chunk.text
                msg.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

# =================== CHART ===================
elif menu == "Chart Absensi":
    st.header("Chart Data Absensi", divider="gray")

    # Ambil data absensi
    data = list(collection.find())
    today = datetime.now(timezone.utc)

    # Konversi waktu + validasi
    for d in data:
        waktu_raw = d.get("waktu", "")
        try:
            d["waktu_parsed"] = pd.to_datetime(waktu_raw, errors="coerce", utc=True)
        except Exception as e:
            st.warning(f"Data error pada {d.get('nama', 'Tidak dikenal')}: {e}")
            d["waktu_parsed"] = None

    # Filter data
    bulan_ini = today.month
    tahun_ini = today.year

    daily_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].date() == today.date()]
    weekly_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"] >= today - timedelta(days=7)]
    monthly_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].month == bulan_ini and d["waktu_parsed"].year == tahun_ini]
    yearly_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].year == tahun_ini]

    # Fungsi untuk menghitung jumlah status absensi
    def hitung_status(data):
        hadir = len([d for d in data if d.get("status") == "Hadir"])
        terlambat = len([d for d in data if d.get("status") == "Terlambat"])
        tidak_hadir = len([d for d in data if d.get("status") == "Tidak Hadir"])
        return hadir, terlambat, tidak_hadir

    # Hitung status untuk setiap kategori
    hadir_daily, terlambat_daily, tidak_hadir_daily = hitung_status(daily_data)
    hadir_weekly, terlambat_weekly, tidak_hadir_weekly = hitung_status(weekly_data)
    hadir_monthly, terlambat_monthly, tidak_hadir_monthly = hitung_status(monthly_data)
    hadir_yearly, terlambat_yearly, tidak_hadir_yearly = hitung_status(yearly_data)

    # Buat DataFrame untuk grafik
    bar_data = {
        "Kategori": ["Hari Ini", "Minggu Ini", "Bulan Ini", "Tahun Ini"],
        "Jumlah": [len(daily_data), len(weekly_data), len(monthly_data), len(yearly_data)],
        "Hadir": [hadir_daily, hadir_weekly, hadir_monthly, hadir_yearly],
        "Terlambat": [terlambat_daily, terlambat_weekly, terlambat_monthly, terlambat_yearly],
        "Tidak Hadir": [tidak_hadir_daily, tidak_hadir_weekly, tidak_hadir_monthly, tidak_hadir_yearly]
    }

    # Membuat DataFrame untuk grafik
    df_bar = pd.DataFrame(bar_data)

    # Menambahkan kolom 'Tooltip' untuk menampilkan informasi tambahan saat hover
    df_bar['Tooltip'] = df_bar.apply(
        lambda row: f"Hadir: {row['Hadir']} | Terlambat: {row['Terlambat']} | Tidak Hadir: {row['Tidak Hadir']}", axis=1)

    # Plot bar chart
    st.subheader("📊 Rekap Absensi Tahunan", divider=True)

    fig = px.bar(df_bar, x="Kategori", y="Jumlah", title="Absensi Berdasarkan Waktu",
                hover_data={"Kategori": False, "Jumlah": False, "Tooltip": True})  # Menambahkan tooltip pada hover
    fig.update_traces(hovertemplate=df_bar['Tooltip'])

    st.plotly_chart(fig)
    
        # =================== Chart Status Pie ===================
    st.subheader("📊 Rekap Absensi Berdasarkan Rentang Tanggal", divider=True)

    # Memilih rentang tanggal
    start_date = st.date_input("Pilih tanggal mulai", min_value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Pilih tanggal selesai", min_value=start_date)

    # Memfilter data berdasarkan rentang tanggal yang dipilih
    data_filtered = [d for d in data if d["waktu_parsed"] and start_date <= d["waktu_parsed"].date() <= end_date]

    # Jika ada data setelah filter, hitung status absensi
    if data_filtered:
        hadir_filtered, terlambat_filtered, tidak_hadir_filtered = hitung_status(data_filtered)

        # Menyusun data untuk grafik
        chart_filtered_data = {
            "Kategori": ["Hadir", "Terlambat", "Tidak Hadir"],
            "Jumlah": [hadir_filtered, terlambat_filtered, tidak_hadir_filtered]
        }
        df_filtered = pd.DataFrame(chart_filtered_data)

        # Membuat grafik batang
        fig = px.bar(df_filtered, x="Kategori", y="Jumlah", title="Rekap Absensi dari {} hingga {}".format(start_date, end_date))
        st.plotly_chart(fig)
    else:
        st.warning("Data absensi untuk rentang tanggal yang dipilih tidak ditemukan.")


    # =================== Chart Status Pie ===================
    status_count = {}
    for d in data:
        status = d.get("status", "Tidak Diketahui")
        status_count[status] = status_count.get(status, 0) + 1
    df_status = pd.DataFrame({"Status": list(status_count.keys()), "Jumlah": list(status_count.values())})
    st.subheader("📊 Persentase Status Absensi", divider=True)
    st.plotly_chart(px.pie(df_status, values="Jumlah", names="Status", title="Persentase Status Absensi"))

    # =================== Chart Absensi Harian per Jam ===================
    st.subheader("📈 Distribusi Absensi Hari Ini per Jam", divider=True)
    df_daily = pd.DataFrame(daily_data)
    if not df_daily.empty:
        df_daily["waktu"] = pd.to_datetime(df_daily["waktu"], errors="coerce", utc=True)
        df_daily["Jam"] = df_daily["waktu"].dt.hour
        jam_group = df_daily.groupby("Jam").size().reset_index(name="Jumlah")
        fig_daily = px.line(jam_group, x="Jam", y="Jumlah", markers=True, title="Absensi Hari Ini per Jam")
        st.plotly_chart(fig_daily)
    else:
        st.info("Belum ada data absensi untuk hari ini.")


    # =================== Chart Mingguan ===================
    st.subheader("📈 Distribusi Absensi Minggu Ini", divider=True)
    df_weekly = pd.DataFrame(weekly_data)
    if not df_weekly.empty:
        df_weekly["waktu"] = pd.to_datetime(df_weekly["waktu"], errors="coerce", utc=True)
        df_weekly["Tanggal"] = df_weekly["waktu"].dt.date
        minggu_group = df_weekly.groupby("Tanggal").size().reset_index(name="Jumlah")
        fig_weekly = px.line(minggu_group, x="Tanggal", y="Jumlah", markers=True, title="Absensi Mingguan")
        st.plotly_chart(fig_weekly)
    else:
        st.info("Belum ada data absensi untuk minggu ini.")


    # =================== Chart Bulanan ===================
    st.subheader("📈 Distribusi Absensi Bulan Ini", divider=True)
    df_monthly = pd.DataFrame(monthly_data)
    if not df_monthly.empty:
        df_monthly["waktu"] = pd.to_datetime(df_monthly["waktu"], errors="coerce", utc=True)
        df_monthly["Tanggal"] = df_monthly["waktu"].dt.date
        bulan_group = df_monthly.groupby("Tanggal").size().reset_index(name="Jumlah")
        fig_monthly = px.line(bulan_group, x="Tanggal", y="Jumlah", markers=True, title="Absensi Bulanan")
        st.plotly_chart(fig_monthly)
    else:
        st.info("Belum ada data absensi untuk bulan ini.")
        
    # =================== Chart  Tergantung tanggal ===================
            
# =================== Filter Rentang Waktu ===================
    st.subheader("📆 Pilih Rentang Waktu untuk Statistik Absensi", divider=True)

    # Pilihan rentang waktu
    waktu_filter = st.selectbox(
        "Pilih rentang waktu:",
        ["Tanggal", "Minggu", "Bulan", "Tahun"]
    )

    # Input berdasarkan pilihan
    if waktu_filter == "Tanggal":
        tanggal_statistik = st.date_input("Pilih tanggal:")
        data_filtered = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].date() == tanggal_statistik]

    elif waktu_filter == "Minggu":
        minggu_statistik = st.slider("Pilih minggu:", 1, 52, 1)
        minggu_start = datetime(today.year, 1, 1) + timedelta(weeks=minggu_statistik - 1)
        minggu_end = minggu_start + timedelta(days=6)
        data_filtered = [d for d in data if d["waktu_parsed"] and minggu_start.date() <= d["waktu_parsed"].date() <= minggu_end.date()]

    elif waktu_filter == "Bulan":
        bulan_statistik = st.selectbox("Pilih bulan:", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], index=today.month-1)
        data_filtered = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].month == bulan_statistik]

    else:  # Tahun
        tahun_statistik = st.number_input("Pilih tahun:", min_value=2000, max_value=2100, value=today.year)
        data_filtered = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].year == tahun_statistik]

    # =================== Chart Berdasarkan Filter ===================
    if data_filtered:
        df_filtered = pd.DataFrame(data_filtered)

        # Buat Chart sesuai data yang sudah difilter
        status_count_filtered = df_filtered["status"].value_counts().reset_index()
        status_count_filtered.columns = ["Status", "Jumlah"]
        fig_filtered = px.pie(status_count_filtered, values="Jumlah", names="Status",
                            title=f"Status Absensi pada {waktu_filter} yang dipilih")

        st.plotly_chart(fig_filtered)

        # Bar jumlah total absensi
        total_absen = len(df_filtered)
        st.metric(label="📋 Total Absensi", value=total_absen)
    else:
        st.info(f"Tidak ada data absensi untuk {waktu_filter} yang dipilih.")




            # =================== Tombol Download Rekap CSV ===================
    # =================== Tombol Download Rekap CSV dengan Filter ===================
    st.subheader("⬇️ Download Rekap Absensi (CSV)", divider=True)

    # Pilihan filter
    filter_opsi = st.selectbox(
        "Pilih data yang ingin direkap:",
        ["Hari Ini", "Minggu Ini", "Bulan Ini", "Semua", "Pilih Tanggal Tertentu"]
    )

    # Jika pilih tanggal tertentu, munculkan date picker
    if filter_opsi == "Pilih Tanggal Tertentu":
        tanggal_dipilih = st.date_input("Pilih tanggal yang ingin didownload:")
        df_download = pd.DataFrame([d for d in data if d["waktu_parsed"] and d["waktu_parsed"].date() == tanggal_dipilih])
    elif filter_opsi == "Hari Ini":
        df_download = pd.DataFrame(daily_data)
    elif filter_opsi == "Minggu Ini":
        df_download = pd.DataFrame(weekly_data)
    elif filter_opsi == "Bulan Ini":
        df_download = pd.DataFrame(monthly_data)
    else:
        df_download = pd.DataFrame(data)
        
    # Format dan download
    if not df_download.empty:
        df_download["waktu"] = pd.to_datetime(df_download["waktu"], errors="coerce", utc=True)
        df_download = df_download[["nama", "kelas", "status", "waktu"]]
        df_download.columns = ["Nama", "Kelas", "Status", "Waktu"]

        csv = df_download.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"rekap_absensi_{filter_opsi.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Tidak ada data yang tersedia untuk filter ini.")





