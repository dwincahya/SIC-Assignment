from datetime import datetime
import time
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://juanditoyeftapriatama:jyp120707@cluster0.rmdy1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["sekolah"]
collection = db["kehadiran"]

# Informasi Ubidots
UBIDOTS_TOKEN = os.getenv("TOKEN_UBI")
DEVICE_LABEL = "as608"

# Fungsi untuk mengirim data ke Ubidots
def kirim_ke_ubidots(data):
    try:
        status = data.get("status", "alpha").lower()
        waktu = data.get("waktu", "")
        if not waktu:
            print(f"Data {data.get('nama', '')} tidak memiliki waktu yang valid. Lewati.")
            return

        # Konversi waktu ke timestamp
        if isinstance(waktu, datetime):
            timestamp = int(waktu.timestamp() * 1000)
        elif isinstance(waktu, str):
            try:
                waktu_obj = datetime.strptime(waktu, "%Y-%m-%dT%H:%M:%SZ")
                timestamp = int(waktu_obj.timestamp() * 1000)
            except ValueError:
                print(f"Format waktu tidak valid untuk {data.get('nama', '')}: {waktu}")
                return
        else:
            print(f"Waktu tidak valid untuk data {data.get('nama', '')}. Lewati.")
            return

        # Konversi status jadi label dan nilai
        if status == "hadir":
            variable_label = "hadir"
            value = 1
        elif status in ["tidak hadir", "alpha", "izin"]:
            variable_label = "tidak_hadir"
            value = 2
        elif status == "terlambat":
            variable_label = "terlambat"
            value = 3
        else:
            variable_label = "lainnya"
            value = 0

        # Siapkan payload
        payload = {
            variable_label: {
                "value": value,
                "timestamp": timestamp,
                "context": {
                    "nama": data.get("nama", ""),
                    "kelas": data.get("kelas", ""),
                    "status": data.get("status", "")
                }
            }
        }

        url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
        headers = {
            "X-Auth-Token": UBIDOTS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if variable_label in result and result[variable_label][0].get("status_code") == 201:
            print(f"Sukses: {data.get('nama', '')} - {status}")
        else:
            print(f"Gagal kirim: {data.get('nama', '')} - Status code: {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print(f"Error saat mengirim data {data.get('nama', '')}: {e}")

# Loop semua data dari MongoDB dan kirim ke Ubidots
def kirim_semua_data():
    print("Mulai mengirim data ke Ubidots...\n")
    for doc in collection.find():
        kirim_ke_ubidots(doc)
        time.sleep(3)
    print("\nSelesai mengirim semua data.")

# Jalankan
if __name__ == "__main__":
    kirim_semua_data()
