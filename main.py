import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

# Import Semua Halaman UI
from ui.login import MainWindow as LoginPage
from ui.register import RegisterPage
from ui.beranda import HomePage
from ui.booking import BookingPage
from ui.detail_booking import DetailBookingPage
from ui.pembayaran import PembayaranPage
from ui.notif_sukses import NotifSuksesPage
from ui.history import HistoryPage 
from ui.pengaturan import PengaturanPage 

# Import Fungsi Database
from database.db_manager import (init_db, get_booked_slots, save_booking, 
                                   get_user_bookings, delete_user_booking, update_user_profile)

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
    
    login_page = LoginPage()
    register_page = RegisterPage()
    home_page = HomePage()
    booking_page = BookingPage()
    detail_page = DetailBookingPage()
    pembayaran_page = PembayaranPage()
    sukses_page = NotifSuksesPage()
    history_page = HistoryPage()  
    pengaturan_page = PengaturanPage() 
    
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(register_page)
    stacked_widget.addWidget(home_page)
    stacked_widget.addWidget(booking_page)
    stacked_widget.addWidget(detail_page)
    stacked_widget.addWidget(pembayaran_page)
    stacked_widget.addWidget(sukses_page)
    stacked_widget.addWidget(history_page)  
    stacked_widget.addWidget(pengaturan_page)  
    
    # PERBAIKAN: Menambahkan sesi sementara untuk tanggal
    current_session = {
        "nama": "",
        "temp_lapangan": "",
        "temp_tanggal": "",
        "temp_slots": [],
        "temp_harga": 0
    }
    
    # --- FUNGSI-FUNGSI NAVIGASI HALAMAN ---
    def buka_halaman_register():
        stacked_widget.setCurrentWidget(register_page)
        stacked_widget.setWindowTitle("SportBook - Register")
        
    def buka_halaman_login():
        stacked_widget.setCurrentWidget(login_page)
        stacked_widget.setWindowTitle("SportBook - Login")
        
    def buka_halaman_beranda():
        stacked_widget.setCurrentWidget(home_page)
        stacked_widget.setWindowTitle("SportBook - Beranda")
        try: home_page.scroll.verticalScrollBar().setValue(0)
        except AttributeError: pass

    def buka_halaman_booking():
        stacked_widget.setCurrentWidget(booking_page)
        stacked_widget.setWindowTitle("SportBook - Booking")
        try: booking_page.scroll.verticalScrollBar().setValue(0)
        except AttributeError: pass
            
    def buka_halaman_history():
        user_aktif = current_session["nama"]
        data_history = get_user_bookings(user_aktif)
        
        history_page.user_name.setText(user_aktif)
        history_page.load_history(data_history)
        
        stacked_widget.setCurrentWidget(history_page)
        stacked_widget.setWindowTitle("SportBook - Riwayat")
        try: history_page.scroll.verticalScrollBar().setValue(0)
        except AttributeError: pass

    def buka_halaman_pengaturan(*args):
        pengaturan_page.inp_nama.clear()
        pengaturan_page.inp_pass.clear()
        pengaturan_page.inp_conf_pass.clear()
        
        stacked_widget.setCurrentWidget(pengaturan_page)
        stacked_widget.setWindowTitle("SportBook - Pengaturan Akun")
        try: pengaturan_page.scroll.verticalScrollBar().setValue(0)
        except AttributeError: pass
        
    # --- FUNGSI LOGIKA DAN TRANSAKSI ---

    def proses_logout():
        current_session["nama"] = ""
        current_session["temp_lapangan"] = ""
        current_session["temp_tanggal"] = ""
        current_session["temp_slots"] = []
        buka_halaman_login()

    def simpan_pengaturan(nama_baru, pwd, conf_pwd):
        if pwd != "" or conf_pwd != "":
            if pwd != conf_pwd:
                QMessageBox.warning(pengaturan_page, "Peringatan", "Konfirmasi Kata Sandi tidak cocok!")
                return
        
        old_nama = current_session["nama"]
        final_nama = nama_baru.strip() if nama_baru.strip() != "" else old_nama

        update_user_profile(old_nama, final_nama, pwd)
        current_session["nama"] = final_nama
        
        home_page.user_name.setText(final_nama)
        home_page.h_title.setText(f"Hallo, <b style='color:#22C55E;'>{final_nama}!</b>")
        booking_page.user_name.setText(final_nama)
        history_page.user_name.setText(final_nama)
        
        QMessageBox.information(pengaturan_page, "Sukses", "Perubahan profil berhasil disimpan secara permanen!")
        buka_halaman_beranda()

    def hapus_riwayat(lapangan_nama, tanggal):
        # PERBAIKAN: Menghapus riwayat harus membutuhkan spesifik tanggal juga
        user_aktif = current_session["nama"]
        delete_user_booking(user_aktif, lapangan_nama, tanggal)
        buka_halaman_history()

    def saat_login_berhasil(nama_user):
        current_session["nama"] = nama_user 
        home_page.user_name.setText(nama_user)
        home_page.h_title.setText(f"Hallo, <b style='color:#22C55E;'>{nama_user}!</b>")
        booking_page.user_name.setText(nama_user)
        buka_halaman_beranda()

    def buka_detail_lapangan(nama, img_name, harga):
        # PERBAIKAN: Selalu ambil tanggal hari ini (default) saat kartu lapangan diklik
        today_str = datetime.now().strftime("%d %B %Y")
        booked = get_booked_slots(nama, today_str)
        detail_page.load_data(nama, img_name, harga, booked)
        stacked_widget.setCurrentWidget(detail_page)
        stacked_widget.setWindowTitle(f"SportBook - {nama}")

    def refresh_jam_berdasarkan_tanggal(lapangan_nama, tanggal_baru):
        # DITAMBAHKAN: Memuat ulang jam jika dropdown diganti
        booked = get_booked_slots(lapangan_nama, tanggal_baru)
        detail_page.refresh_slots(booked)

    def lanjut_ke_pembayaran(lapangan_nama, list_jam, total_harga, tanggal):
        current_session["temp_lapangan"] = lapangan_nama
        current_session["temp_slots"] = list_jam
        current_session["temp_harga"] = total_harga
        current_session["temp_tanggal"] = tanggal
        
        jumlah_jam = len(list_jam)
        pembayaran_page.load_data(jumlah_jam, total_harga)
        stacked_widget.setCurrentWidget(pembayaran_page)
        stacked_widget.setWindowTitle("SportBook - Pembayaran")

    def proses_pembayaran_final(metode):
        user_aktif = current_session["nama"]
        lapangan = current_session["temp_lapangan"]
        slots = current_session["temp_slots"]
        tanggal = current_session["temp_tanggal"]
        
        # PERBAIKAN: Save booking sekarang melempar parameter tanggal
        sukses = save_booking(user_aktif, lapangan, tanggal, slots)
        if sukses:
            current_session["temp_slots"] = []
            stacked_widget.setCurrentWidget(sukses_page)
            stacked_widget.setWindowTitle("SportBook - Transaksi Berhasil")
        else:
            QMessageBox.critical(pembayaran_page, "Error", "Gagal menyimpan jadwal ke database.")
    
    # --- HUBUNGAN SIGNAL DAN SLOT (NAVIGASI & AKSI) ---
    
    login_page.footer_link.clicked.connect(buka_halaman_register)
    register_page.f_link.clicked.connect(buka_halaman_login)
    login_page.login_successful.connect(saat_login_berhasil)
    register_page.register_successful.connect(buka_halaman_login)

    home_page.btn_booking.clicked.connect(buka_halaman_booking)
    home_page.btn_hist.clicked.connect(buka_halaman_history)
    home_page.btn_settings.clicked.connect(buka_halaman_pengaturan)
    
    booking_page.btn_home.clicked.connect(buka_halaman_beranda)
    booking_page.btn_hist.clicked.connect(buka_halaman_history)
    booking_page.btn_settings.clicked.connect(buka_halaman_pengaturan)
    booking_page.btn_back.clicked.connect(buka_halaman_beranda)
    
    history_page.btn_home.clicked.connect(buka_halaman_beranda)
    history_page.btn_booking.clicked.connect(buka_halaman_booking)
    history_page.btn_settings.clicked.connect(buka_halaman_pengaturan)
    history_page.btn_back.clicked.connect(buka_halaman_beranda)

    pengaturan_page.btn_home.clicked.connect(buka_halaman_beranda)
    pengaturan_page.btn_booking.clicked.connect(buka_halaman_booking)
    pengaturan_page.btn_hist.clicked.connect(buka_halaman_history)

    def buat_label_bisa_diklik(label_widget):
        label_widget.setCursor(Qt.PointingHandCursor)
        label_widget.mousePressEvent = buka_halaman_pengaturan

    buat_label_bisa_diklik(home_page.user_name)
    buat_label_bisa_diklik(home_page.icon_user)
    buat_label_bisa_diklik(booking_page.user_name)
    buat_label_bisa_diklik(booking_page.icon_user)
    buat_label_bisa_diklik(history_page.user_name)
    buat_label_bisa_diklik(history_page.icon_user)

    pengaturan_page.save_clicked.connect(simpan_pengaturan)
    pengaturan_page.logout_clicked.connect(proses_logout)

    history_page.request_delete.connect(hapus_riwayat)
    
    home_page.request_book.connect(buka_detail_lapangan)
    booking_page.request_book.connect(buka_detail_lapangan)
    
    detail_page.go_back.connect(buka_halaman_booking)
    detail_page.proceed_checkout.connect(lanjut_ke_pembayaran)
    # DITAMBAHKAN: Sambungan signal saat ganti tanggal
    detail_page.request_date_change.connect(refresh_jam_berdasarkan_tanggal)
    
    pembayaran_page.go_back.connect(lambda: stacked_widget.setCurrentWidget(detail_page))
    pembayaran_page.confirm_payment.connect(proses_pembayaran_final)
    sukses_page.back_to_home.connect(buka_halaman_beranda)
    
    # --- KONFIGURASI AWAL WINDOW ---
    stacked_widget.setWindowTitle("SportBook")
    stacked_widget.setMinimumSize(800, 500)
    stacked_widget.resize(1000, 600)
    
    buka_halaman_login()
    stacked_widget.show()
    sys.exit(app.exec())