from data import users
import re


def _angka(teks):
    return teks.isascii() and teks.isdigit()


def kumpulkan(*hasil):
    return [pesan for pesan in hasil if pesan]


def parse_angka(teks, label, minimal=1, pesan_minimal=None, maksimal=None, pesan_maksimal=None):
    teks = teks.strip()
    if teks == "":
        return None, f"{label} Tidak boleh kosong!"
    if not _angka(teks):
        return None, f"{label} Harus berupa angka bulat!"
    nilai = int(teks)
    if nilai < minimal:
        return None, pesan_minimal or f"{label} minimal {minimal}!"
    if maksimal is not None and nilai > maksimal:
        return None, pesan_maksimal or f"{label} maksimal {maksimal}!"
    return nilai, None

def cek_teks_wajib(teks, label):
    if teks.strip() == "":
        return f"{label} Tidak boleh kosong!"
    return None


def cek_nama(nama, kecuali=None):
    if nama.strip() == "":
        return "Nama tidak boleh kosong!"
    if nama.strip().isdigit():
        return "Nama tidak boleh hanya berisi angka!"
    for pemilik in users:
        if pemilik != kecuali and pemilik.lower() == nama.lower():
            return "Nama sudah digunakan akun lain!"
    return None


def cek_umur(umur):
    if not _angka(umur):
        return "Umur harus berupa angka!"
    if int(umur) < 18:
        return "Umur minimal 18 tahun!"
    return None


def cek_nik(nik):
    if not _angka(nik) or len(nik) != 16:
        return "NIK harus berupa angka 16 digit!"
    if any(akun["nik"] == nik for akun in users.values()):
        return "NIK sudah terdaftar!"
    return None


def cek_no_hp(no_hp):
    if not _angka(no_hp) or not 10 <= len(no_hp) <= 13:
        return "No. HP harus berupa angka 10-13 digit!"
    if not no_hp.startswith("08"):
        return "No. HP harus diawali 08!"
    return None


def cek_alamat(alamat):
    return cek_teks_wajib(alamat, "Alamat")


def cek_password_baru(password):
    if password.strip() == "":
        return "Password tidak boleh kosong"
    return None


def cek_tipe_huruf(teks):
    if teks == "":
        return "Tipe tidak boleh kosong."
    if not re.fullmatch(r"[A-Za-z ]+", teks):
        return "Tipe hanya boleh berisi huruf"
    return None