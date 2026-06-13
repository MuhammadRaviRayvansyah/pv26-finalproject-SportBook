import sys
import os
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox

from ui.login import MainWindow as LoginPage
from ui.register import RegisterPage
from ui.beranda import HomePage
from ui.booking import BookingPage
from ui.detail_booking import DetailBookingPage # Import UI Baru

# Import database
from database.db_manager import init_db, get_booked_slots, save_booking

def load_stylesheet(app, file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    
    style_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    load_stylesheet(app, style_path)
    
    stacked_widget = QStackedWidget()
    
    # Instance Halaman
    login_page = LoginPage()
    register_page = RegisterPage()
    home_page = HomePage()
    booking_page = BookingPage()
    detail_page = DetailBookingPage() # Instance Baru
    
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(register_page)
    stacked_widget.addWidget(home_page)
    stacked_widget.addWidget(booking_page)
    stacked_widget.addWidget(detail_page)
    
    # Variabel Sesi untuk menyimpan user yang sedang login
    current_session = {"nama": ""}
    
    # --- FUNGSI NAVIGASI ---
    def buka_halaman_register():
        stacked_widget.setCurrentWidget(register_page)
        
    def buka_halaman_login():
        stacked_widget.setCurrentWidget(login_page)
        
    def buka_halaman_beranda():
        stacked_widget.setCurrentWidget(home_page)
        home_page.scroll.verticalScrollBar().setValue(0)

    def buka_halaman_booking():
        stacked_widget.setCurrentWidget(booking_page)
        booking_page.scroll.verticalScrollBar().setValue(0)
        
    def saat_login_berhasil(nama_user):
        current_session["nama"] = nama_user # Simpan sesi
        home_page.user_name.setText(nama_user)
        home_page.h_title.setText(f"Hallo, <b style='color:#22C55E;'>{nama_user}!</b>")
        booking_page.user_name.setText(nama_user)
        buka_halaman_beranda()

    def buka_detail_lapangan(nama, img_name, harga):
        """Dipanggil saat tombol 'Booking Lapangan' pada Card ditekan."""
        # Ambil data jam yang sudah dibooking dari SQLite
        booked = get_booked_slots(nama)
        # Muat data UI
        detail_page.load_data(nama, img_name, harga, booked)
        
        stacked_widget.setCurrentWidget(detail_page)
        detail_page.scroll.verticalScrollBar().setValue(0)

    def proses_checkout_sementara(lapangan_nama, list_jam, total_harga):
        """Dipanggil saat menekan 'Berikutnya' di halaman Detail."""
        user_aktif = current_session["nama"]
        
        # Simpan ke Database
        sukses = save_booking(user_aktif, lapangan_nama, list_jam)
        
        if sukses:
            jam_str = "\n".join(list_jam)
            QMessageBox.information(detail_page, "Sukses", 
                f"Booking Berhasil Disimpan!\n\nLapangan: {lapangan_nama}\nTotal: Rp {total_harga:,.0f}\nJam:\n{jam_str}")
            # Kembali ke beranda setelah sukses
            buka_halaman_beranda()
        else:
            QMessageBox.critical(detail_page, "Error", "Gagal menyimpan jadwal ke database.")
    
    # --- MENGHUBUNGKAN SIGNAL ---
    login_page.footer_link.clicked.connect(buka_halaman_register)
    register_page.f_link.clicked.connect(buka_halaman_login)
    
    login_page.login_successful.connect(saat_login_berhasil)
    register_page.register_successful.connect(buka_halaman_login)

    home_page.btn_booking.clicked.connect(buka_halaman_booking)
    booking_page.btn_back.clicked.connect(buka_halaman_beranda)
    booking_page.btn_home.clicked.connect(buka_halaman_beranda)
    
    # Koneksi Signal dari Card ke fungsi buka_detail_lapangan
    home_page.request_book.connect(buka_detail_lapangan)
    booking_page.request_book.connect(buka_detail_lapangan)
    
    # Koneksi Signal dari Detail Page
    detail_page.go_back.connect(buka_halaman_booking)
    detail_page.proceed_checkout.connect(proses_checkout_sementara)
    
    stacked_widget.setMinimumSize(800, 500)
    stacked_widget.resize(1000, 600)
    
    buka_halaman_login()
    stacked_widget.show()
    sys.exit(app.exec())