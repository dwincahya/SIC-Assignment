import ujson

def load_nama():
    try:
        with open("data.json", "r") as f:
            return ujson.load(f)
    except:
        return {}

def simpan_nama(ID, nama, kelas):
    data = load_nama()
    data[str(ID)] = {
        "nama": nama,
        "kelas": kelas
    }
    with open("data.json", "w") as f:
        ujson.dump(data, f)

def get_nama(ID):
    data = load_nama()
    return data.get(str(ID), {"nama": f"ID {ID}", "kelas": "Unknown"})
