# SportBook

## Aplikasi Pemesanan Lapangan Olahraga Desktop Berbasis PySide6

### Deskripsi Singkat

SportBook adalah aplikasi desktop yang dikembangkan menggunakan Python dan PySide6 untuk memudahkan proses pemesanan lapangan olahraga. Aplikasi ini menyediakan fitur registrasi dan login pengguna, pemesanan lapangan berdasarkan slot waktu, simulasi pembayaran, riwayat pemesanan, pengaturan akun, serta panel administrasi untuk mengelola data booking dan melihat statistik penggunaan.

### Fitur Utama

* Login dan registrasi akun
* Sistem autentikasi User dan Admin
* Pemesanan lapangan olahraga
* Pemilihan slot waktu yang tersedia
* Simulasi pembayaran (GoPay, OVO, DANA)
* Riwayat pemesanan
* Pengaturan akun pengguna
* Dashboard Admin dengan statistik dan grafik
* Manajemen booking oleh Admin
* Export data booking ke CSV
* Database SQLite

---

## Anggota Kelompok

| Nama                     | NIM         |
| ------------------------ | ----------- |
| Muhammad Ravi Rayvansyah | F1D02410078 |
| Yudhi Fajar Pratama      | F1D02310142 |
| M. Danuarta Wiraguna     | F1D02310124 |

---

## Cara Menjalankan Program

### 1. Clone Repository

```bash
git clone <url-repository>
cd SportBook
```

### 2. Install Dependency

```bash
pip install PySide6
pip install PySide6-Charts
pip install pandas
pip install fpdf
```

Atau:

```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```bash
python main.py
```

### 4. Login

#### Admin

Admin
234567

#### User

Lakukan registrasi terlebih dahulu melalui menu Register.

---

## Struktur Folder

```text
SportBook/
│
├── assets/
├── database/
│   ├── sportbook.db
│   └── db_manager.py
│
├── styles/
│   └── style.qss
│
├── ui/
│   ├── login.py
│   ├── register.py
│   ├── beranda.py
│   ├── booking.py
│   ├── detail_booking.py
│   ├── pembayaran.py
│   ├── notif_sukses.py
│   ├── history.py
│   ├── pengaturan.py
│   ├── admin_dashboard.py
│   ├── admin_manage_bookings.py
│   ├── admin_sidebar.py
│   └── admin_pengaturan.py
│
└── main.py
```

---

## Screenshot Aplikasi

### Login

![Login](<img width="577" height="279" alt="image" src="https://github.com/user-attachments/assets/74ac5c60-33ba-4826-9cad-0338ba840bf6" />
)

### Register

![Register](<img width="577" height="279" alt="image" src="https://github.com/user-attachments/assets/5cc9ffb5-804c-4049-a470-4d796092a28b" />
)

### Beranda

![Beranda](<img width="577" height="278" alt="image" src="https://github.com/user-attachments/assets/33c1a53d-0085-4d87-8b41-ebb6110730b7" />
)

### Daftar Lapangan

![Booking](<img width="650" height="315" alt="image" src="https://github.com/user-attachments/assets/43da1ebe-c468-4887-b4d2-5e289615c840" />
)

### Detail Booking

![Detail Booking](<img width="644" height="309" alt="image" src="https://github.com/user-attachments/assets/b06020f4-82c2-4b17-9714-1876eb9b4ed5" />
)

### Pembayaran

![Pembayaran](<img width="638" height="306" alt="image" src="https://github.com/user-attachments/assets/baceeeea-8370-49f9-976d-45e899182652" />
)

### Notifikasi Sukses

![Sukses](<img width="638" height="311" alt="image" src="https://github.com/user-attachments/assets/c9374d01-2056-4cbb-80fe-f4ae0dbdc326" />
)

### Riwayat Pemesanan

![History](<img width="664" height="322" alt="image" src="https://github.com/user-attachments/assets/f9c362dc-a98e-49ff-8cb9-7df78a472adf" />
)

### Pengaturan Akun

![Pengaturan](<img width="663" height="321" alt="image" src="https://github.com/user-attachments/assets/65d49af5-0a64-4bbf-92de-d9f50d7db9ae" />
)

### Dashboard Admin

![Dashboard Admin](<img width="663" height="322" alt="image" src="https://github.com/user-attachments/assets/9f7451c9-bf9b-4fe1-8af4-9ac750470143" />
)

### Kelola Booking

![Kelola Booking](<img width="663" height="320" alt="image" src="https://github.com/user-attachments/assets/a0e65feb-2275-4b01-8bd8-6ee8d81458db" />
)

---

## Pembagian Tugas

### Muhammad Ravi Rayvansyah (F1D02410078)

**Backend & Database**

* database/db_manager.py
* main.py
* ui/login.py
* ui/register.py

Tanggung jawab:

* Perancangan database SQLite
* CRUD database
* Sistem login dan registrasi
* Session management
* Navigasi aplikasi
* Integrasi antar halaman

### Yudhi Fajar Pratama (F1D02310142)

**Modul Transaksi**

* ui/booking.py
* ui/detail_booking.py
* ui/pembayaran.py
* ui/notif_sukses.py
* styles/style.qss

Tanggung jawab:

* Daftar lapangan
* Detail booking
* Pemilihan slot waktu
* Simulasi pembayaran
* Halaman transaksi berhasil
* Styling antarmuka aplikasi

### M. Danuarta Wiraguna (F1D02310124)

**Halaman Utama & Admin**

* ui/beranda.py
* ui/history.py
* ui/pengaturan.py
* ui/admin_dashboard.py
* ui/admin_manage_bookings.py
* ui/admin_sidebar.py
* ui/admin_pengaturan.py

Tanggung jawab:

* Beranda pengguna
* Riwayat pemesanan
* Pengaturan akun
* Dashboard admin
* Manajemen booking
* Sidebar admin
* Pengaturan admin

---

## Teknologi yang Digunakan

* Python
* PySide6
* QtCharts
* SQLite
* Pandas
* FPDF

---

## Mata Kuliah

Pemrograman Visual
Program Studi Teknik Informatika
Fakultas Teknik
Universitas Mataram
Tahun 2026
