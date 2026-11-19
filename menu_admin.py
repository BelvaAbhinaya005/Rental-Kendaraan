from data import users, transaksi
<<<<<<< Updated upstream
from tampilan import (bersihkan_layar, banner, tekan_enter, pilih, konfirmasi,
                        tampilkan_tabel, rupiah, format_tanggal)
=======
from tampilan import (bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, tampilkan_tabel, rupiah, format_tanggal)
>>>>>>> Stashed changes
from kendaraan import pengelolaan_kendaraan

STATUS_TRANSAKSI = ["Berjalan", "Selesai"]

def tabel_transaksi(daftar):
    baris = []
    for t in daftar:
        baris.append([
            t["id"], t["customer"], t["kendaraan"], f"{t['lama_sewa']} hari",
            format_tanggal(t["tanggal_sewa"]), rupiah(t["total_biaya"]),
            rupiah(t["dp"]), rupiah(t["pelunasan"]), rupiah(t["denda"]), t["status"],
        ])
    tampilkan_tabel(
        ["ID", "Customer", "Kendaraan", "Lama Sewa", "Tanggal Sewa",
        "Total Biaya", "DP", "Pelunasan", "Denda", "Status"],
        baris,
    )


def akun_customer():
    bersihkan_layar()
    banner("AKUN CUSTOMER")

    daftar = []                      
    for nama, akun in users.items():
        if akun["role"] == "user":
            daftar.append((nama, akun))

    if len(daftar) == 0:
        print("Belum ada akun customer.")
        tekan_enter()
        return

    baris = []
    opsi = []
    nomor = 1
    for nama, akun in daftar:
        baris.append([nomor, nama, akun["umur"], akun["nik"], akun["no_hp"],
                    akun["alamat"], rupiah(akun["saldo"])])
        opsi.append(f"{nomor}. {nama}")
        nomor += 1
    opsi.append("Kembali")

    tampilkan_tabel(["No", "Nama", "Umur", "NIK", "No. HP", "Alamat", "Saldo"], baris)
    print()

    pilihan = pilih("Pilih customer yang akan dihapus", opsi)
    if pilihan == len(opsi):       
        return
    nama, akun = daftar[pilihan - 1]

    for t in transaksi:
        if t["nik"] == akun["nik"] and t["status"] == "Berjalan":
            print("\nCustomer masih memiliki transaksi berjalan!")
            tekan_enter()
            return

    if konfirmasi(f"Yakin ingin menghapus akun {nama}?"):
        del users[nama]
        print("\nAkun customer berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan.")
    tekan_enter()


def diagram_transaksi():
    if len(transaksi) == 0:
        print("\nBelum ada data transaksi untuk dibuat diagram.")
        tekan_enter()
        return

    jumlah_berjalan = 0
    jumlah_selesai = 0
    for t in transaksi:
        if t["status"] == "Berjalan":
            jumlah_berjalan += 1
        else:
            jumlah_selesai += 1

    import matplotlib.pyplot as plt

    nama_status = ["Berjalan", "Selesai"]
    jumlah = [jumlah_berjalan, jumlah_selesai]

    plt.bar(nama_status, jumlah, color=["#f0a030", "#3a9d5d"])
    plt.title("Jumlah Transaksi Rental per Status")
    plt.xlabel("Status Transaksi")
    plt.ylabel("Jumlah Transaksi")
    plt.yticks(range(0, max(jumlah) + 2))

    print("\nDiagram tampil di jendela baru. Tutup jendelanya untuk melanjutkan.")
    plt.show()
    tekan_enter()


def transaksi_rental():
    while True:
        bersihkan_layar()
        banner("TRANSAKSI RENTAL")
        pilihan = pilih("Pilih menu", [
            "1. Semua Transaksi",
            "2. Filter Berdasarkan Status",
            "3. Diagram Transaksi",
            "4. Kembali",
        ])

        if pilihan == 1:
            print()
            if len(transaksi) == 0:
                print("Belum ada data transaksi.")
            else:
                tabel_transaksi(transaksi)
            tekan_enter()

        elif pilihan == 2:
            status = STATUS_TRANSAKSI[pilih("Pilih status", ["1. Berjalan", "2. Selesai"]) - 1]
            hasil = []
            for t in transaksi:
                if t["status"] == status:
                    hasil.append(t)
            print()
            if len(hasil) == 0:
                print("Tidak ada transaksi dengan status tersebut.")
            else:
                tabel_transaksi(hasil)
            tekan_enter()

        elif pilihan == 3:
            diagram_transaksi()

        else:
            break


def menu_admin():
    while True:
        bersihkan_layar()
        banner("MENU ADMIN")
        pilihan = pilih("Pilih menu", [
            "1. Pengelolaan Kendaraan",
            "2. Transaksi Rental",
            "3. Akun Customer",
            "4. Keluar",
        ])
        if pilihan == 1:
            pengelolaan_kendaraan()
        elif pilihan == 2:
            transaksi_rental()
        elif pilihan == 3:
            akun_customer()
        else:
            break