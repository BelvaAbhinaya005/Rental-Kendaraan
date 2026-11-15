from data import users


def cek_angka(teks):
    return teks.isascii() and teks.isdigit()


def kumpulkan(*hasil):
    daftar_error = []
    for pesan in hasil:
        if pesan:
            daftar_error.append(pesan)
    return daftar_error


def parse_angka(teks, label, minimal=1):
    teks = teks.strip()
    if teks == "":
        return None, f"{label} tidak boleh kosong!"
    if not cek_angka(teks):
        return None, f"{label} harus berupa angka bulat!"
    nilai = int(teks)
    if nilai < minimal:
        return None, f"{label} minimal {minimal}!"
    return nilai, None


def cek_teks_wajib(teks, label):
    if teks.strip() == "":
        return f"{label} tidak boleh kosong!"
    return None


def cek_nama(nama, kecuali=None):
    if nama.strip() == "":
        return "Nama tidak boleh kosong!"
    for pemilik in users:
        if pemilik != kecuali and pemilik.lower() == nama.lower():
            return "Nama sudah digunakan akun lain!"
    return None


def cek_umur(umur):
    if not cek_angka(umur):
        return "Umur harus berupa angka!"
    if int(umur) < 18:
        return "Umur minimal 18 tahun!"
    return None


def cek_nik(nik):
    if not cek_angka(nik) or len(nik) != 16:
        return "NIK harus berupa angka 16 digit!"
    for akun in users.values():
        if akun["nik"] == nik:
            return "NIK sudah terdaftar!"
    return None


def cek_no_hp(no_hp):
    if not cek_angka(no_hp) or len(no_hp) < 10 or len(no_hp) > 13:
        return "No. HP harus berupa angka 10-13 digit!"
    if not no_hp.startswith("08"):
        return "No. HP harus diawali 08!"
    return None


def cek_alamat(alamat):
    return cek_teks_wajib(alamat, "Alamat")


def cek_password_baru(password):
    if password.strip() == "":
        return "Password tidak boleh kosong!"
    return None
