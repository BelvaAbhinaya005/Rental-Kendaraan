from tampilan import bersihkan_layar, banner, pilih
<<<<<<< HEAD
from autentikasi import login, register, lupa_password
=======
>>>>>>> cd4b96aea8c4bc5261132a36e6550f1ba00469ca

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
<<<<<<< HEAD
                login()
            elif pilihan == 2:
                register()
            elif pilihan == 3:
                lupa_password()
=======
                print("Fitur login belum tersedia.")
            elif pilihan == 2:
                print("Fitur daftar akun belum tersedia.")
            elif pilihan == 3:
                print("Fitur lupa password belum tersedia.")
>>>>>>> cd4b96aea8c4bc5261132a36e6550f1ba00469ca
            else:
                break
    except (KeyboardInterrupt, EOFError):
        print()

    bersihkan_layar()
    print("Bye-bye!")

if __name__ == "__main__":
    main()
