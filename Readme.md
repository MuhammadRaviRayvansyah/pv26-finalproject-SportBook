# SportBook - Sistem Manajemen Booking Lapangan Olahraga

## Deskripsi Singkat
SportBook adalah aplikasi desktop berbasis antarmuka grafis (GUI) yang dibangun menggunakan pustaka PySide6 (Python). Aplikasi ini dirancang untuk mendigitalisasi proses penyewaan lapangan olahraga, memudahkan pengguna dalam memesan jadwal, dan membantu pengelola (Admin) dalam mengelola data transaksi menggunakan database lokal SQLite.

---

## Anggota Kelompok
Proyek ini dikembangkan untuk memenuhi tugas mata kuliah oleh:

| Nama Lengkap | NIM |
| :--- | :--- |
| Muhammad Ravi Rayvansyah | F1D02410078 |
| Yudhi Fajar Pratama | F1D02310142 |
| M. Danuarta Wiraguna | F1D02310124 |

---

## Pembagian Tugas

1. Muhammad Ravi Rayvansyah (Fullstack Developer - Core System)
Mengerjakan keseluruhan sistem inti dan kode aplikasi (kecuali bagian Admin), meliputi:
* UI/UX & Logika Utama: Merancang seluruh antarmuka aplikasi menggunakan PySide6, termasuk halaman Login, Register, Beranda User, Pengaturan, dan Layout Responsif.
* Database & Fungsionalitas: Membangun sistem autentikasi, logika booking jadwal, manajemen tabel riwayat (termasuk soft delete), serta logika untuk mencetak data transaksi.
* Keamanan Aplikasi: Memastikan semua form tervalidasi dengan baik agar terhindar dari crash (error handling via QMessageBox).

2. Yudhi Fajar Pratama (Admin Interface Developer)
Mengerjakan kode untuk bagian antarmuka khusus pengelola, meliputi:
* Admin Dashboard & Sidebar: Mendesain dan mengimplementasikan antarmuka navigasi Sidebar Admin serta halaman Dashboard Admin agar pengelola dapat memonitor, mencari, dan mengelola seluruh data transaksi booking.

3. M. Danuarta Wiraguna (Technical Writer / Penyusun Laporan)
Bertanggung jawab penuh atas penyusunan dokumentasi tugas, meliputi:
* Penyusunan Laporan Proyek: Menulis, merangkum, dan menyusun dokumen laporan akhir proyek (makalah) secara komprehensif untuk diserahkan kepada dosen penilai sebagai syarat kelengkapan tugas (tidak berpartisipasi dalam penulisan kode program).

---

## Cara Menjalankan Aplikasi

Prasyarat Sistem:
* Python 3.8 atau versi yang lebih baru.
* Koneksi internet untuk mengunduh pustaka.

Langkah-langkah Eksekusi:
1. Ekstrak folder proyek ini ke dalam komputer Anda.
2. Buka terminal atau command prompt, lalu arahkan ke folder utama proyek.
3. Install pustaka dependencies yang dibutuhkan dengan menjalankan perintah berikut: pip install PySide6 fpdf
4. Jalankan aplikasi dengan perintah: python main.py

---

## Screenshot Aplikasi

1. Halaman Login & Registrasi
![Halaman Login](assets/screenshots/image.png)
![Halaman Register](assets/screenshots/image-1.png)

2. Dashboard User & Form Booking
![Dashboard User](assets/screenshots/image-2.png)
![Form Booking](assets/screenshots/image-3.png)

3. Panel Admin & Fitur Cetak PDF
![Panel Admin](assets/screenshots/image-4.png)
![Fitur Cetak PDF](assets/screenshots/image-5.png)