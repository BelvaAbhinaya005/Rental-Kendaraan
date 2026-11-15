from tampilan import bersihkan_layar, banner, pilih

def main():
    try:
        while True:
            bersihkan_layar()
            banner("RentGo - Rental dan Go")
            pilihan = pilih("Pilih menu", [
                "1. Login",
                "2. Daftar Akun",
                "3. Lupa Password",
                "4. Keluar",
            ])
            if pilihan == 1:
                print("Fitur login belum tersedia.")
            elif pilihan == 2:
                print("Fitur daftar akun belum tersedia.")
            elif pilihan == 3:
                print("Fitur lupa password belum tersedia.")
            else:
                break
    except (KeyboardInterrupt, EOFError):
        print()

    bersihkan_layar()
    print("Bye-bye!")

if __name__ == "__main__":
    main()
