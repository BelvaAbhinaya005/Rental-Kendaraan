from waktu import MULAI_PROGRAM, HARI

DP_PERSEN = 50
DENDA_PERSEN_PER_HARI = 50

users = {
    "admin1": {
        "nik": "6401010101900001",
        "umur": 30, 
        "no_hp": "081200000001",
        "alamat": "Jl. Merdeka No. 1",
        "password": "admin123",
        "role": "admin",
        "saldo": 0,
    },   
    "admin2": {
        "nik": "6401010101900002",
        "umur": 27, 
        "no_hp": "0812000000023",
        "alamat": "Jl. Ahmad Yani",
        "password": "admin123",
        "role": "admin",
        "saldo": 0,
    },
    "Belva": {
        "nik": "6401010101900005",
        "umur": 18,
        "no_hp": "081349645233",
        "alamat": "Gg. Alam Segar 2",
        "password": "Belva123",
        "role": "user",
        "saldo": 0,
    },
    "Hendra" : {
        "nik": "6401010101900011",
        "umur": 18,
        "no_hp": "083813414951",
        "alamat": "Gg. Melati",
        "password": "Hendra123",
        "role": "user",
        "saldo": 1000000,
    },
    "Kahfi" : {
        "nik": "6401010101900013",
        "umur": 18,
        "no_hp": "085822305525",
        "alamat": "Gg. Perjuangan 7",
        "password": "Kahfi123",
        "role": "user",
        "saldo": 2000000,
    },
    "Ferdi" : {
        "nik": "6401010101900018",
        "umur": 18,
        "no_hp": "081528627868",
        "alamat": "MT Haryono",
        "password": "Ferdi123",
        "role": "user",
        "saldo": 500000,
    },
}

kendaraan = [
    {"id": 1, "tipe": "Mobil", "merek": "Toyota Avanza",    "harga": 350000, "status": "Tersedia"},
    {"id": 2, "tipe": "Mobil", "merek": "Honda Brio",       "harga": 300000, "status": "Tersedia"},
    {"id": 3, "tipe": "Mobil", "merek": "Mitsubishi Xpander", "harga": 400000, "status": "Tersedia"},
    {"id": 4, "tipe": "Motor", "merek": "Honda Vario 125",  "harga": 100000, "status": "Tersedia"},
    {"id": 5, "tipe": "Motor", "merek": "Yamaha NMAX",      "harga": 150000, "status": "Tersedia"},
    {"id": 6, "tipe": "Motor", "merek": "Honda Beat",       "harga": 80000,  "status": "Tersedia"},
]

transaksi = [
    {
        "id": "TRX-001", "nik": "6401010101950001", "customer": "user1",
        "id_kendaraan": 1, "kendaraan": "Toyota Avanza (Mobil)", "harga_per_hari": 350000,
        "lama_sewa": 2, "waktu_sewa": MULAI_PROGRAM - 10 * HARI,
        "waktu_kembali": MULAI_PROGRAM - 8 * HARI,
        "total_biaya": 700000, "dp": 350000, "pelunasan": 350000,
        "denda": 0, "status": "Selesai",
    },
    {
        "id": "TRX-002", "nik": "6401010101950002", "customer": "user2",
        "id_kendaraan": 3, "kendaraan": "Mitsubishi Xpander (Mobil)", "harga_per_hari": 400000,
        "lama_sewa": 3, "waktu_sewa": MULAI_PROGRAM - 5.5 * HARI,
        "waktu_kembali": None,
        "total_biaya": 1200000, "dp": 600000, "pelunasan": 600000,
        "denda": 0, "status": "Berjalan",
    },
    {
        "id": "TRX-003", "nik": "6401010101950001", "customer": "user1",
        "id_kendaraan": 5, "kendaraan": "Yamaha NMAX (Motor)", "harga_per_hari": 150000,
        "lama_sewa": 5, "waktu_sewa": MULAI_PROGRAM - 1 * HARI,
        "waktu_kembali": None,
        "total_biaya": 750000, "dp": 375000, "pelunasan": 375000,
        "denda": 0, "status": "Berjalan",
    },
]

sesi = {"nama": None}

counter = {"kendaraan": 6, "transaksi": 3}


def cari_akun(identitas):
    if identitas in users:
        return identitas, users[identitas]
    for nama, akun in users.items():
        if akun["nik"] == identitas:
            return nama, akun
    return None