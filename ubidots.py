from datetime import datetime
import requests
from pymongo import MongoClient

client = MongoClient("mongodb+srv://juanditoyeftapriatama:jyp120707@cluster0.rmdy1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["sekolah"]
collection = db["kehadiran"]

UBIDOTS_TOKEN = "BBUS-qYYE4dG2jcJ9ukaLr68roB831Nlsd9"
DEVICE_LABEL = "as608"

def kirim_ke_ubidots(data):
    status = data.get("status", "alpha").lower()
    waktu = data.get("waktu", "")
    timestamp = int(datetime.strptime(waktu, "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000)

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
    requests.post(url, headers=headers, json=payload)
