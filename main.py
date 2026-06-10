import sys
import os
from PySide6.QtWidgets import QApplication, QStackedWidget

# Mengimport seluruh halaman dari modul ui
# Catatan: login.py menggunakan class MainWindow sesuai permintaan Anda sebelumnya
from ui.login import MainWindow as LoginPage
from ui.register import RegisterPage
from ui.beranda import HomePage

def load_stylesheet(app, file_path):
    """Memuat file QSS untuk styling detail seluruh komponen."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    else:
        print(f"Peringatan: File stylesheet tidak ditemukan di {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Memuat stylesheet agar seluruh dekorasi visual tetap diaplikasikan
    style_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    load_stylesheet(app, style_path)
    
    # Menggunakan QStackedWidget sebagai container utama window aplikasi
    stacked_widget = QStackedWidget()
    
    # Inisialisasi masing-masing object halaman
    login_page = LoginPage()
    register_page = RegisterPage()
    home_page = HomePage()
    
    # Memasukkan halaman ke dalam stack widget
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(register_page)
    stacked_widget.addWidget(home_page)
    
    # --- FUNGSI NAVIGASI ---
    def buka_halaman_register():
        stacked_widget.setCurrentWidget(register_page)
        stacked_widget.setWindowTitle("SportBook - Register")

    def buka_halaman_login():
        stacked_widget.setCurrentWidget(login_page)
        stacked_widget.setWindowTitle("SportBook - Login")
        
    def buka_halaman_beranda():
        stacked_widget.setCurrentWidget(home_page)
        stacked_widget.setWindowTitle("SportBook - Beranda")
    
    # --- MENGHUBUNGKAN TOMBOL DENGAN NAVIGASI ---
    # 1. Navigasi Login <-> Register melalui teks link di footer
    login_page.footer_link.clicked.connect(buka_halaman_register)
    register_page.f_link.clicked.connect(buka_halaman_login)
    
    # 2. Navigasi menuju Beranda saat tombol aksi ditekan
    login_page.btn_masuk.clicked.connect(buka_halaman_beranda)
    register_page.btn_submit.clicked.connect(buka_halaman_beranda)
    
    # Konfigurasi ukuran window utama
    stacked_widget.setMinimumSize(800, 500)
    stacked_widget.resize(1000, 600)
    
    # Set tampilan awal agar membuka halaman login terlebih dahulu
    buka_halaman_login()
    
    # Tampilkan aplikasi
    stacked_widget.show()
    sys.exit(app.exec())