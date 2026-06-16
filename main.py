import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt

# Import Semua Halaman UI (User)
from ui.login import MainWindow as LoginPage
from ui.register import RegisterPage
from ui.beranda import HomePage
from ui.booking import BookingPage
from ui.detail_booking import DetailBookingPage
from ui.pembayaran import PembayaranPage
from ui.notif_sukses import NotifSuksesPage
from ui.history import HistoryPage 
from ui.pengaturan import PengaturanPage 

# Import Semua Halaman UI (Admin)
from ui.admin_sidebar import AdminSidebar
from ui.admin_dashboard import AdminDashboard
from ui.admin_manage_fields import AdminManageFields
from ui.admin_field_form import AdminFieldForm
from ui.admin_manage_categories import AdminManageCategories
from ui.admin_manage_bookings import AdminManageBookings

# Import Fungsi Database
from database.db_manager import (init_db, get_booked_slots, save_booking, 
                                   get_user_bookings, delete_user_booking, update_user_profile,
                                   get_all_fields)

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
    
    # --- INISIALISASI HALAMAN USER ---
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

    # --- INISIALISASI HALAMAN ADMIN ---
    admin_main_page = QWidget()
    admin_main_layout = QHBoxLayout(admin_main_page)
    admin_main_layout.setContentsMargins(0, 0, 0, 0)
    admin_main_layout.setSpacing(0)
    
    admin_sidebar = AdminSidebar()
    admin_stacked = QStackedWidget()
    
    admin_dashboard = AdminDashboard()
    admin_fields = AdminManageFields()
    admin_field_form = AdminFieldForm()
    admin_categories = AdminManageCategories()
    admin_bookings = AdminManageBookings()
    
    admin_stacked.addWidget(admin_dashboard)
    admin_stacked.addWidget(admin_fields)
    admin_stacked.addWidget(admin_field_form)
    admin_stacked.addWidget(admin_categories)
    admin_stacked.addWidget(admin_bookings)
    
    admin_main_layout.addWidget(admin_sidebar)
    admin_main_layout.addWidget(admin_stacked)
    
    stacked_widget.addWidget(admin_main_page)
    
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
        # DITAMBAHKAN: Refresh data lapangan agar dinamis
        home_page.load_dynamic_fields(get_all_fields())
        stacked_widget.setCurrentWidget(home_page)
        stacked_widget.setWindowTitle("SportBook - Beranda")
        try: home_page.scroll.verticalScrollBar().setValue(0)
        except AttributeError: pass

    def buka_halaman_booking():
        # DITAMBAHKAN: Refresh data lapangan agar dinamis
        booking_page.load_dynamic_fields(get_all_fields())
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
    
    def buka_admin_panel():
        admin_dashboard.refresh_data()
        admin_sidebar.set_active("dashboard")
        admin_stacked.setCurrentWidget(admin_dashboard)
        stacked_widget.setCurrentWidget(admin_main_page)
        stacked_widget.setWindowTitle("SportBook - Admin Panel")
        
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

    def saat_login_berhasil(nama_user, role_user):
        current_session["nama"] = nama_user 
        if role_user == "admin":
            buka_admin_panel()
        else:
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

    # --- LOGIKA NAVIGASI ADMIN ---

    def navigasi_admin(target):
        if target == "dashboard":
            admin_dashboard.refresh_data()
            admin_stacked.setCurrentWidget(admin_dashboard)
        elif target == "fields":
            admin_fields.load_data()
            admin_stacked.setCurrentWidget(admin_fields)
        elif target == "bookings":
            admin_bookings.load_data()
            admin_stacked.setCurrentWidget(admin_bookings)
        elif target == "categories":
            admin_categories.load_data()
            admin_stacked.setCurrentWidget(admin_categories)
        elif target == "logout":
            proses_logout()

    def buka_tambah_lapangan():
        admin_field_form.load_form(None)
        admin_stacked.setCurrentWidget(admin_field_form)

    def buka_edit_lapangan(data):
        admin_field_form.load_form(data)
        admin_stacked.setCurrentWidget(admin_field_form)

    def simpan_lapangan_sukses():
        admin_fields.load_data()
        admin_stacked.setCurrentWidget(admin_fields)
    
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
    detail_page.request_date_change.connect(refresh_jam_berdasarkan_tanggal)
    
    pembayaran_page.go_back.connect(lambda: stacked_widget.setCurrentWidget(detail_page))
    pembayaran_page.confirm_payment.connect(proses_pembayaran_final)
    sukses_page.back_to_home.connect(buka_halaman_beranda)

    # --- SIGNAL ADMIN ---
    admin_sidebar.nav_changed.connect(navigasi_admin)
    admin_fields.request_add.connect(buka_tambah_lapangan)
    admin_fields.request_edit.connect(buka_edit_lapangan)
    admin_field_form.go_back.connect(lambda: admin_stacked.setCurrentWidget(admin_fields))
    admin_field_form.save_success.connect(simpan_lapangan_sukses)
    
    # --- KONFIGURASI AWAL WINDOW ---
    stacked_widget.setWindowTitle("SportBook")
    stacked_widget.setMinimumSize(800, 500)
    stacked_widget.resize(1000, 600)
    
    buka_halaman_login()
    stacked_widget.show()
    sys.exit(app.exec())