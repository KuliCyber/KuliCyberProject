import pyfiglet
import os
import time
import requests
import json

class Colors:
    """Kelas untuk mendefinisikan kode warna ANSI."""
    RESET = '\033[0m'
    BRIGHT_CYAN = '\033[96m' 
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_RED = '\033[91m' # Ditambahkan untuk pesan error

# --- 2. Fungsi Tampilan Banner ---
def print_ascii_art(text, font="slant", color=Colors.BRIGHT_CYAN):
    """Mencetak teks ASCII art dengan warna."""
    try:
        ascii_art = pyfiglet.figlet_format(text, font=font)
        print(color + ascii_art + Colors.RESET)
    except Exception as e:
        # Fallback jika pyfiglet gagal
        print(f"\n{color}--- {text} ---{Colors.RESET}")

def tampilkan_banner():
    """Menampilkan banner OSINT saat skrip dimulai."""
    # Membersihkan terminal (berfungsi di Linux/macOS/Windows)
    os.system('cls' if os.name == 'nt' else 'clear') 
    
    team_name = "KULLICYBERTEAM"
    tagline = "OSINT NAVIGATION INTELLIGENCE"
    
    print(f"\n{Colors.BRIGHT_GREEN}<<< INITIATING OSINT TOOLBOX >>>{Colors.RESET}\n")

    print_ascii_art(team_name, font="slant", color=Colors.BRIGHT_CYAN)
    
    print_ascii_art(tagline, font="small", color=Colors.BRIGHT_MAGENTA)
    
    print(f"{Colors.BRIGHT_GREEN}--- TOOLBOX SIAP DIGUNAKAN ---\n{Colors.RESET}")
    time.sleep(1) # Jeda sedikit agar banner terlihat

# --- 3. Fungsi Pencarian OSINT (Sherlock) ---
def cari_akun_osint(username):
    """Mencari nama pengguna di ratusan platform media sosial menggunakan Sherlock CLI."""
    print(f"\n{Colors.BRIGHT_CYAN}[+] Mencari akun untuk username: {username}...{Colors.RESET}")
    print(f"{Colors.BRIGHT_GREEN}[INFO] Ini membutuhkan package 'sherlock' terinstal. Jika error, coba instal: pip install sherlock{Colors.RESET}")
    
    try:
        # Menghapus timeout karena sudah ada di konfigurasi Sherlock default atau menggunakan default 5s
        # Menjalankan perintah Sherlock
        os.system(f"sherlock --timeout 15 {username}") # Timeout ditingkatkan menjadi 15 detik
        
        print(f"\n{Colors.BRIGHT_GREEN}[+] Pencarian selesai. Detail tautan disimpan dalam file teks (nama_pengguna.txt) di folder saat ini.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}[!] Terjadi kesalahan saat menjalankan Sherlock: {e}{Colors.RESET}")

# --- 4. Fungsi Geolocation IP Address ---
def cari_lokasi_ip(ip_address):
    """Mencari Geolocation (negara, kota, ISP) dari IP Address."""
    print(f"\n{Colors.BRIGHT_CYAN}[+] Mencari lokasi untuk IP: {ip_address}...{Colors.RESET}")
    # Menggunakan HTTPS untuk koneksi yang lebih aman
    api_url = f"http://ip-api.com/json/{ip_address}" 
    
    try:
        # Menggunakan timeout 5 detik untuk permintaan HTTP
        response = requests.get(api_url, timeout=5) 
        response.raise_for_status() # Akan memunculkan error untuk status kode 4xx/5xx
        data = response.json()
        
        if data.get('status') == 'success':
            print(f"\n{Colors.BRIGHT_MAGENTA}[--- HASIL GEOLOCATION IP ---]{Colors.RESET}")
            print(f"   {Colors.BRIGHT_GREEN}IP Address{Colors.RESET}   : {data.get('query')}")
            print(f"   {Colors.BRIGHT_GREEN}Negara{Colors.RESET}       : {data.get('country')} ({data.get('countryCode')})")
            print(f"   {Colors.BRIGHT_GREEN}Kota{Colors.RESET}         : {data.get('city')}")
            print(f"   {Colors.BRIGHT_GREEN}Kode Pos{Colors.RESET}     : {data.get('zip')}")
            print(f"   {Colors.BRIGHT_GREEN}Zona Waktu{Colors.RESET}   : {data.get('timezone')}")
            print(f"   {Colors.BRIGHT_GREEN}ISP/Organisasi{Colors.RESET}: {data.get('isp')} / {data.get('org')}")
            print(f"   {Colors.BRIGHT_GREEN}Koordinat{Colors.RESET}    : Lat {data.get('lat')}, Lon {data.get('lon')}")
            print(f"{Colors.BRIGHT_MAGENTA}------------------------------{Colors.RESET}")
        else:
            print(f"{Colors.BRIGHT_RED}[!] Gagal menemukan data untuk IP: {ip_address} (Status: {data.get('message', 'Unknown error')}){Colors.RESET}")
            
    except requests.exceptions.Timeout:
        print(f"{Colors.BRIGHT_RED}[!] Gagal terhubung ke API Geolocation: Request Timeout (Lebih dari 5 detik).{Colors.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Colors.BRIGHT_RED}[!] Gagal terhubung ke API Geolocation atau kesalahan lain: {e}{Colors.RESET}")
    except json.JSONDecodeError:
        print(f"{Colors.BRIGHT_RED}[!] Gagal memproses respons API (bukan JSON).{Colors.RESET}")

# --- 5. Fungsi Utama & Menu ---
def menu_utama():
    """Menampilkan menu dan menjalankan fungsi berdasarkan pilihan pengguna."""
    tampilkan_banner() # Panggil banner saat menu dimulai

    while True:
        print(f"\n{Colors.BRIGHT_CYAN}=============================={Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}  TOOLBOX OSINT SEDERHANA {Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}=============================={Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}1. Pencarian OSINT (Berdasarkan Username - Menggunakan Sherlock){Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}2. Geolocation IP Address (Cari Lokasi){Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}3. Keluar{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}------------------------------{Colors.RESET}")
        
        pilihan = input(f"{Colors.BRIGHT_MAGENTA}Masukkan pilihan Anda (1-3): {Colors.RESET}")
        
        if pilihan == '1':
            username = input("Masukkan Username yang dicari: ")
            cari_akun_osint(username)
        elif pilihan == '2':
            print("\n[INFO] Perlu IP Address Target (Contoh: 8.8.8.8)")
            ip_address = input("Masukkan IP Address: ")
            cari_lokasi_ip(ip_address)
        elif pilihan == '3':
            print(f"\n{Colors.BRIGHT_MAGENTA}Terima kasih telah menggunakan Toolbox. Sampai jumpa!{Colors.RESET}")
            break
        else:
            print(f"{Colors.BRIGHT_RED}[!] Pilihan tidak valid. Silakan coba lagi.{Colors.RESET}")

# --- 6. Eksekusi Skrip ---
if __name__ == "__main__":
    try:
        # Cek apakah pyfiglet dan requests terinstal
        import pyfiglet # Cek ulang untuk memastikan
        import requests # Cek ulang untuk memastikan
        menu_utama()
    except ImportError as e:
        print(f"{Colors.BRIGHT_RED}\n[KRITIS] Perlu menginstal modul penting: {e.name}.{Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}Silakan jalankan: pip install pyfiglet requests{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}\n[KRITIS] Terjadi kesalahan tidak terduga: {e}{Colors.RESET}")
