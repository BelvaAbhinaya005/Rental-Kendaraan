from data import users, sesi, cari_akun
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, input_password
from validasi_input import kumpulkan, cek_nama, cek_umur, cek_nik, cek_no_hp, cek_alamat, cek_password_baru
from menu_admin import menu_admin
from menu_user import menu_user

MAKS_PERCOBAAN = 3


def register():
    bersihkan_layar()
    banner("REGISTER")
    print("Persyaratan data:")
    print("  Nama     : tidak boleh kosong, belum dipakai akun lain")
    print("  Umur     : angka, minimal 18")
    print("  NIK      : angka, 16 digit, belum terdaftar")
    print("  No. HP   : angka, 10-13 digit, diawali 08")
    print("  Alamat   : tidak boleh kosong")
    print("  Password : tidak boleh kosong\n")

    nama = input("Nama     : ").strip() 
    umur = input("Umur     : ").strip()
    nik = input("NIK      : ").strip()
    no_hp = input("No. HP   : ").strip()
    alamat = input("Alamat   : ").strip()

    daftar_error = kumpulkan(cek_nama(nama), cek_umur(umur), cek_nik(nik), cek_no_hp(no_hp), cek_alamat(alamat))
    if daftar_error:
        print()
        for pesan in daftar_error:
            print("Error:", pesan)
        tekan_enter()
        return

    password = input_password("Password ")
    error_password = cek_password_baru(password)
    if error_password:
        print("\nError:", error_password)
        tekan_enter()
        return

    users[nama] = {
        "nik": nik,
        "umur": int(umur),
        "no_hp": no_hp,
        "alamat": alamat,
        "password": password,
        "role": "user",
        "saldo": 0,
    }
    print("\nRegistrasi berhasil! Silakan login.")
    tekan_enter()


def lupa_password():
    bersihkan_layar()
    banner("LUPA PASSWORD")
    nama = input("Nama : ").strip()
    nik = input("NIK  : ").strip()

    if nama not in users or users[nama]["nik"] != nik:
        print("\nError: Nama dan NIK tidak cocok dengan akun manapun!")
        tekan_enter()
        return

    password_baru = input_password("Password baru")
    error_password = cek_password_baru(password_baru)
    if error_password:
        print("\nError:", error_password)
        tekan_enter()
        return

    users[nama]["password"] = password_baru
    print("\nPassword berhasil diubah! Silakan login.")
    tekan_enter()


def login():
    percobaan = 0
    while True:
        bersihkan_layar()

        if percobaan == MAKS_PERCOBAAN:
            banner("LOGIN")
            print(f"Login gagal {MAKS_PERCOBAAN}x.\n")
            if pilih("Lupa password?", ["1. Ya", "2. Tidak"]) == 1:
                lupa_password()
            return

        banner("LOGIN")
        identitas = input("Nama / NIK : ").strip()
        password = input_password("Password  ")

        hasil = cari_akun(identitas)
        if hasil is not None and hasil[1]["password"] == password:
            nama, akun = hasil
            sesi["nama"] = nama
            print(f"\nLogin berhasil! Selamat datang, {nama} ({akun['role']})")
            tekan_enter()

            if akun["role"] == "admin":
                menu_admin()
            else:
                menu_user()

            sesi["nama"] = None
            return

        percobaan += 1
        print("\nError: Nama/NIK atau password salah!")
        tekan_enter()