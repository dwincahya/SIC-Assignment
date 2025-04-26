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
    st.title("🤖 Chatbot Absensi Siswa (Gemini)")
    
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
    daily_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"].date() == today.date()]
    weekly_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"] >= today - timedelta(days=7)]
    monthly_data = [d for d in data if d["waktu_parsed"] and d["waktu_parsed"] >= today - timedelta(days=30)]

    # =================== Chart Jumlah Harian/Mingguan/Bulanan ===================
    bar_data = {
        "Kategori": ["Hari Ini", "Minggu Ini", "Bulan Ini"],
        "Jumlah": [len(daily_data), len(weekly_data), len(monthly_data)]
    }
    df_bar = pd.DataFrame(bar_data)
    st.subheader("📊 Statistik Absensi Berdasarkan Waktu")
    st.plotly_chart(px.bar(df_bar, x="Kategori", y="Jumlah", title="Absensi Berdasarkan Waktu"))

    # =================== Chart Status Pie ===================
    status_count = {}
    for d in data:
        status = d.get("status", "Tidak Diketahui")
        status_count[status] = status_count.get(status, 0) + 1
    df_status = pd.DataFrame({"Status": list(status_count.keys()), "Jumlah": list(status_count.values())})
    st.subheader("📊 Persentase Status Absensi")
    st.plotly_chart(px.pie(df_status, values="Jumlah", names="Status", title="Persentase Status Absensi"))

    # =================== Chart Absensi Harian per Jam ===================
    st.subheader("📈 Distribusi Absensi Hari Ini per Jam")
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
    st.subheader("📈 Distribusi Absensi Minggu Ini")
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
    st.subheader("📈 Distribusi Absensi Bulan Ini")
    df_monthly = pd.DataFrame(monthly_data)
    if not df_monthly.empty:
        df_monthly["waktu"] = pd.to_datetime(df_monthly["waktu"], errors="coerce", utc=True)
        df_monthly["Tanggal"] = df_monthly["waktu"].dt.date
        bulan_group = df_monthly.groupby("Tanggal").size().reset_index(name="Jumlah")
        fig_monthly = px.line(bulan_group, x="Tanggal", y="Jumlah", markers=True, title="Absensi Bulanan")
        st.plotly_chart(fig_monthly)
    else:
        st.info("Belum ada data absensi untuk bulan ini.")

