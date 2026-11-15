from datetime import date, timedelta
from data import (users, kendaraan, transaksi, sesi, counter,
                dp_persen, denda_persen_per_hari)
from tampilan import (bersihkan_layar, banner, tekan_enter, pilih, konfirmasi,
                    tampilkan_tabel, cetak_rincian, rupiah, format_tanggal)
from validasi_input import parse_angka
from kelola_akun import kelola_akun

def top_up_saldo():
    akun = users[sesi["nama"]]
    bersihkan_layar()
    banner("TOP UP SALDO")
    print("Saldo saat ini:", rupiah(akun["saldo"]))
    print("Persyaratan nominal: angka bulat, lebih dari 0\n")

    nominal, error = parse_angka(input("Nominal top up: "), "Nominal", minimal=1)
    if error:
        print("\nError:", error)
        tekan_enter()
        return

    akun["saldo"] += nominal
    print("\nTop up berhasil! Saldo Anda sekarang:", rupiah(akun["saldo"]))
    tekan_enter()


def pesan_kendaraan():
    akun = users[sesi["nama"]]
    bersihkan_layar()
    banner("PESAN KENDARAAN")

    tersedia = []
    for k in kendaraan:
        if k["status"] == "Tersedia":
            tersedia.append(k)

    if len(tersedia) == 0:
        print("Belum ada kendaraan yang tersedia.")
        tekan_enter()
        return

    baris = []
    opsi = []
    nomor = 1
    for k in tersedia:
        baris.append([nomor, k["tipe"], k["merek"], rupiah(k["harga"])])
        opsi.append(f"{nomor}. {k['merek']} ({k['tipe']}) - {rupiah(k['harga'])}/hari")
        nomor += 1
    opsi.append("Kembali")

    tampilkan_tabel(["No", "Tipe", "Merek", "Harga Rental / Hari"], baris)
    print()

    pilihan = pilih("Pilih kendaraan yang akan dipesan", opsi)
    if pilihan == len(opsi):         
        return
    kendaraan_dipilih = tersedia[pilihan - 1]

    lama, error = parse_angka(input("\nLama sewa (hari): "), "Lama sewa", minimal=1)
    if error:
        print("\nError:", error)
        tekan_enter()
        return

    total = kendaraan_dipilih["harga"] * lama
    dp = total * dp_persen // 100
    pelunasan = total - dp
    nama_kendaraan = f"{kendaraan_dipilih['merek']} ({kendaraan_dipilih['tipe']})"

    print("\nRingkasan pesanan:")
    cetak_rincian([
        ("Kendaraan", nama_kendaraan),
        ("Harga / Hari", rupiah(kendaraan_dipilih["harga"])),
        ("Lama Sewa", f"{lama} hari"),
        ("Total Biaya", rupiah(total)),
        (f"Wajib DP ({dp_persen}%)", rupiah(dp)),
        (f"Sisa Bayar Saat Kembali ({100 - dp_persen}%)", rupiah(pelunasan)),
        ("Saldo Saat Ini", rupiah(akun["saldo"])),
    ])

    if akun["saldo"] < dp:
        print(f"\nSaldo tidak cukup untuk membayar DP {dp_persen}%! Silakan top up dulu.")
        tekan_enter()
        return

    print()
    if konfirmasi(f"Konfirmasi pemesanan dan bayar DP ({dp_persen}%)?"):
        akun["saldo"] -= dp
        kendaraan_dipilih["status"] = "Disewa"

        counter["transaksi"] += 1
        id_transaksi = f"TRX-{counter['transaksi']:03d}"

        transaksi.append({
            "id": id_transaksi,
            "nik": akun["nik"],
            "customer": sesi["nama"],
            "id_kendaraan": kendaraan_dipilih["id"],
            "kendaraan": nama_kendaraan,
            "harga_per_hari": kendaraan_dipilih["harga"],
            "lama_sewa": lama,
            "tanggal_sewa": date.today(),
            "total_biaya": total,
            "dp": dp,
            "pelunasan": pelunasan,
            "denda": 0,
            "status": "Berjalan",
        })
        print(f"\nPemesanan berhasil! DP {dp_persen}% terbayar.")
        print("ID Transaksi:", id_transaksi)
    else:
        print("\nPemesanan dibatalkan.")
    tekan_enter()

def pengembalian_kendaraan():
    akun = users[sesi["nama"]]
    bersihkan_layar()
    banner("PENGEMBALIAN KENDARAAN")

    berjalan = []
    for t in transaksi:
        if t["nik"] == akun["nik"] and t["status"] == "Berjalan":
            berjalan.append(t)

    if len(berjalan) == 0:
        print("Tidak ada kendaraan yang sedang disewa.")
        tekan_enter()
        return

    baris = []
    opsi = []
    nomor = 1
    for t in berjalan:
        baris.append([nomor, t["id"], t["kendaraan"], format_tanggal(t["tanggal_sewa"]),
                    f"{t['lama_sewa']} hari", rupiah(t["total_biaya"]), rupiah(t["pelunasan"])])
        opsi.append(f"{nomor}. {t['id']} - {t['kendaraan']}")
        nomor += 1
    opsi.append("Kembali")

    tampilkan_tabel(["No", "ID", "Kendaraan", "Tanggal Sewa", "Lama Sewa",
                    "Total Biaya", f"Sisa Pelunasan ({100 - dp_persen}%)"], baris)
    print()

    pilihan = pilih("Pilih transaksi yang dikembalikan", opsi)
    if pilihan == len(opsi):          # Kembali
        return
    trx = berjalan[pilihan - 1]

    jatuh_tempo = trx["tanggal_sewa"] + timedelta(days=trx["lama_sewa"])
    hari_terlambat = (date.today() - jatuh_tempo).days
    if hari_terlambat < 0:
        hari_terlambat = 0
    denda = hari_terlambat * trx["harga_per_hari"] * denda_persen_per_hari // 100
    total_bayar = trx["pelunasan"] + denda

    print("\nRincian tagihan:")
    cetak_rincian([
        ("Kendaraan", trx["kendaraan"]),
        ("Jatuh Tempo", format_tanggal(jatuh_tempo)),
        (f"Sisa Pelunasan ({100 - dp_persen}%)", rupiah(trx["pelunasan"])),
        ("Hari Terlambat", f"{hari_terlambat} hari"),
        ("Denda", rupiah(denda)),
        ("Total yang Harus Dibayar", rupiah(total_bayar)),
        ("Saldo Saat Ini", rupiah(akun["saldo"])),
    ])

    if akun["saldo"] < total_bayar:
        print("\nSaldo tidak cukup untuk melunasi! Silakan top up saldo.")
        tekan_enter()
        return

    print()
    if konfirmasi("Konfirmasi pelunasan dan pengembalian kendaraan?"):
        akun["saldo"] -= total_bayar

        for k in kendaraan:                    
            if k["id"] == trx["id_kendaraan"]:
                k["status"] = "Tersedia"

        trx["status"] = "Selesai"
        trx["denda"] = denda
        print("\nKendaraan berhasil dikembalikan! Terima kasih.")
    else:
        print("\nPengembalian dibatalkan.")
    tekan_enter()


def riwayat_transaksi():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("RIWAYAT TRANSAKSI")

    riwayat = []
    for t in transaksi:
        if t["nik"] == akun["nik"]:
            riwayat.append(t)

    if len(riwayat) == 0:
        print("Belum ada riwayat transaksi.")
    else:
        baris = []
        nomor = 1
        for t in riwayat:
            baris.append([nomor, t["id"], t["kendaraan"], format_tanggal(t["tanggal_sewa"]),
                        f"{t['lama_sewa']} hari", rupiah(t["total_biaya"]),
                        rupiah(t["dp"]), rupiah(t["denda"]), t["status"]])
            nomor += 1
        tampilkan_tabel(["No", "ID", "Kendaraan", "Tanggal Sewa", "Lama Sewa",
                        "Total Biaya", f"DP ({dp_persen}%)", "Denda", "Status"], baris)
    tekan_enter()

def menu_user():
    while True:
        bersihkan_layar()
        banner("MENU USER")
        pilihan = pilih("Pilih menu", [
            "1. Pesan Kendaraan",
            "2. Pengembalian Kendaraan",
            "3. Riwayat Transaksi",
            "4. Top Up Saldo",
            "5. Kelola Akun",
            "6. Keluar",
        ])
        if pilihan == 1:
            pesan_kendaraan()
        elif pilihan == 2:
            pengembalian_kendaraan()
        elif pilihan == 3:
            riwayat_transaksi()
        elif pilihan == 4:
            top_up_saldo()
        elif pilihan == 5:
            kelola_akun()
        else:
            break
