from data import users, transaksi, sesi
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, input_password, tampilkan_tabel, rupiah
from validasi_input import kumpulkan, cek_nama, cek_umur, cek_no_hp, cek_password_baru, cek_alamat


def ubah_password():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("UBAH PASSWORD")
    print("Persyaratan: password baru tidak boleh kosong dan tidak sama dengan yang lama\n")

    lama = input_password("Password lama")
    if lama != akun["password"]:
        print("\nError: Password lama salah!")
        tekan_enter()
        return

    baru = input_password("Password baru")
    if cek_password_baru(baru) or baru == lama:
        print("\nError: Password baru tidak boleh kosong dan tidak boleh sama dengan yang lama!")
        tekan_enter()
        return

    konfirmasi_baru = input_password("Konfirmasi password baru")
    if konfirmasi_baru != baru:
        print("\nError: Konfirmasi password tidak sama dengan password baru!")
        tekan_enter()
        return

    print()
    if konfirmasi("Yakin ingin mengubah password?"):
        akun["password"] = baru
        print("\nPassword berhasil diubah!")
    else:
        print("\nPerubahan password dibatalkan.")
    tekan_enter()


def ubah_data_diri():
    nama_lama = sesi["nama"]
    akun = users[nama_lama]

    bersihkan_layar()
    banner("UBAH DATA DIRI")
    print("Persyaratan:")
    print("  Nama   : belum dipakai akun lain")
    print("  Umur   : angka, minimal 18")
    print("  No. HP : angka, 10-13 digit, diawali 08")
    print("  (NIK tidak bisa diubah)\n")

    print(f"Data saat ini: {nama_lama} - {akun['umur']} tahun - "
          f"{akun['no_hp']} - {akun['alamat']}")
    print("Masukkan data baru (Enter = tidak diubah):")
    nama_baru = input("Nama   : ").strip()
    umur = input("Umur   : ").strip()
    no_hp = input("No. HP : ").strip()
    alamat = input("Alamat : ").strip()

    daftar_error = kumpulkan(
        cek_nama(nama_baru, kecuali=nama_lama) if nama_baru else None,
        cek_umur(umur) if umur else None,
        cek_no_hp(no_hp) if no_hp else None,
        cek_alamat(alamat) if alamat else None,
    )
    if daftar_error:
        print()
        for pesan in daftar_error:
            print("Error:", pesan)
        tekan_enter()
        return

    berubah = False
    if nama_baru:
        users[nama_baru] = users.pop(nama_lama)
        sesi["nama"] = nama_baru
        berubah = True
    if umur:
        akun["umur"] = int(umur)
        berubah = True
    if no_hp:
        akun["no_hp"] = no_hp
        berubah = True
    if alamat:
        akun["alamat"] = alamat
        berubah = True

    print("\nData berhasil diperbarui!" if berubah else "\nTidak ada data yang diubah.")
    tekan_enter()


def kelola_akun():
    while True:
        akun = users[sesi["nama"]]  
        bersihkan_layar()
        banner("KELOLA AKUN")
        tampilkan_tabel(["Data", "Isi"], [
            ["Nama", sesi["nama"]],
            ["Umur", akun["umur"]],
            ["NIK", akun["nik"]],
            ["No. HP", akun["no_hp"]],
            ["Alamat", akun["alamat"]],
            ["Saldo", rupiah(akun["saldo"])],
            ["Password", "*" * len(akun["password"])],
        ])
        print()

        pilihan = pilih("Pilih menu", [
            "1. Ubah Password",
            "2. Ubah Data Diri",
            "3. Kembali",
        ])
        if pilihan == 1:
            ubah_password()
        elif pilihan == 2:
            ubah_data_diri()
        else:
            break