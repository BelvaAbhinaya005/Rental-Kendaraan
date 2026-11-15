import os
import inquirer
import pwinput
from prettytable import PrettyTable

lebar = 56
garis = "=" * lebar


def bersihkan_layar():
    os.system("cls")


def banner(teks):
    print(garis)
    print(teks.center(lebar))
    print(garis)


def tekan_enter(pesan = "Pencet Enter Untuk Lanjutt..."):
    input(f"\n{pesan}")


def pilih(pesan, opsi):
    pertanyaan = [
        inquirer.List("pilihan", message=pesan, choices=opsi, carousel=True)
    ]
    jawaban = inquirer.prompt(pertanyaan, raise_keyboard_interrupt=True)
    teks_dipilih = jawaban["pilihan"]
    nomor = opsi.index(teks_dipilih) + 1
    return nomor


def konfirmasi(pesan):
    hasil = pilih(pesan, ["Ya", "Tidak"])
    if hasil == 1:
        return True
    else:
        return False


def input_password(pesan):
    return pwinput.pwinput(prompt=pesan + ": ", mask="*")


def tampilkan_tabel(kolom, baris):
    tabel = PrettyTable()
    tabel.field_names = kolom
    tabel.align = "l"
    for isi in baris:
        tabel.add_row(isi)
    print(tabel)


def cetak_rincian(baris):
    terpanjang = 0
    for label, nilai in baris:
        if len(label) > terpanjang:
            terpanjang = len(label)

    for label, nilai in baris:
        print("  " + label.ljust(terpanjang) + " : " + str(nilai))


def rupiah(nilai):
    teks = f"{nilai:,}"
    teks = teks.replace(",", ".")
    return "Rp" + teks


def format_tanggal(tanggal):
    return tanggal.strftime("%d-%m-%Y")