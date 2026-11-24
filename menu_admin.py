from data import users, transaksi
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, tampilkan_tabel, rupiah, format_waktu
from kendaraan import pengelolaan_kendaraan
from waktu import waktu_sekarang, nomor_hari, tanggal_hari, MENIT_PER_HARI
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

STATUS_TRANSAKSI = ["Berjalan", "Selesai"]


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


def tabel_transaksi(daftar):
    tampilkan_tabel(
        ["ID", "Nama Customer", "Kendaraan", "Lama Sewa", "Waktu Sewa",
        "Total Biaya", "DP (50%)", "Pelunasan (50%)", "Status"],
        [[t["id"], t["customer"], t["kendaraan"], f"{t['lama_sewa']} hari",
        format_waktu(t["waktu_sewa"]), rupiah(t["total_biaya"]),
        rupiah(t["dp"]), rupiah(t["pelunasan"]), t["status"]]
        for t in daftar],
    )


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
            if not transaksi:
                print("Belum ada data transaksi.")
            else:
                tabel_transaksi(transaksi)
            tekan_enter()

        elif pilihan == 2:
            status = STATUS_TRANSAKSI[pilih("Pilih status", ["1. Berjalan", "2. Selesai"]) - 1]
            hasil = [t for t in transaksi if t["status"] == status]
            print()
            if not hasil:
                print("Tidak ada transaksi dengan status tersebut.")
            else:
                tabel_transaksi(hasil)
            tekan_enter()

        elif pilihan == 3:
            diagram_transaksi()

        else:
            break


def diagram_transaksi():
    if not transaksi:
        print("\nBelum ada data transaksi untuk dibuat diagram.")
        tekan_enter()
        return

    per_hari = {}
    for t in transaksi:
        hari = nomor_hari(t["waktu_sewa"])
        per_hari[hari] = per_hari.get(hari, 0) + 1

    hari_awal = min(per_hari)
    hari_akhir = max(max(per_hari), nomor_hari(waktu_sekarang()))
    daftar_hari = list(range(hari_awal, hari_akhir + 1))

    tanggal = [tanggal_hari(h).strftime("%d-%m-%Y") for h in daftar_hari]
    jumlah = [per_hari.get(h, 0) for h in daftar_hari]

    plt.figure(figsize=(8, 4.5))
    plt.plot(tanggal, jumlah, marker="o", color="blue")
    plt.title("Perkembangan Rental per Hari")
    plt.xlabel(f"Tanggal (setiap {MENIT_PER_HARI:g} menit waktu nyata = 1 hari)")
    plt.ylabel("Jumlah Rental")
    plt.yticks(range(0, max(jumlah) + 2)) 
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    print("\nDiagram ditampilkan di jendela baru. Tutup jendela diagram untuk melanjutkan.")
    plt.show()
    tekan_enter()


def akun_customer():
    bersihkan_layar()
    banner("AKUN CUSTOMER")
    daftar = [(nama, akun) for nama, akun in users.items() if akun["role"] == "user"]
    if not daftar:
        print("Belum ada akun customer.")
        tekan_enter()
        return

    tampilkan_tabel(
        ["No", "Nama", "Umur", "NIK", "No. HP", "Alamat", "Saldo"],
        [[no, nama, akun["umur"], akun["nik"], akun["no_hp"], akun["alamat"], rupiah(akun["saldo"])]
        for no, (nama, akun) in enumerate(daftar, 1)],
    )
    print()

    label = [f"{no}. {nama}" for no, (nama, _) in enumerate(daftar, 1)] + ["Kembali"]
    nomor = pilih("Pilih customer yang akan dihapus", label)
    if nomor == len(label):
        return
    nama, akun = daftar[nomor - 1]

    if any(t["nik"] == akun["nik"] and t["status"] == "Berjalan" for t in transaksi):
        print("\nCustomer memiliki transaksi berjalan")
        tekan_enter()
        return

    if konfirmasi(f"Yakin ingin menghapus akun {nama}?"):
        del users[nama]
        print("\nAkun customer berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan.")
    tekan_enter()
    