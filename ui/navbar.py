import os
from PySide6.QtWidgets import QFrame, QHBoxLayout, QToolButton, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_colored_icon(icon_path, color, size=28):
    pixmap = QPixmap(icon_path)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        painter = QPainter(colored_pixmap)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), color)
        painter.end()
        return QIcon(colored_pixmap)
    return QIcon()

# Buat Kelas Khusus untuk Navbar
class BottomNavbar(QFrame):
    nav_home = Signal()
    nav_booking = Signal()
    nav_history = Signal()
    nav_settings = Signal()

    # PERUBAHAN: Tambahkan parameter active_page dengan default "beranda"
    def __init__(self, active_page="beranda", parent=None):
        super().__init__(parent)
        self.setFixedHeight(75)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white;")
        
        shadow_bot = QGraphicsDropShadowEffect(self)
        shadow_bot.setBlurRadius(20)
        shadow_bot.setXOffset(0)
        shadow_bot.setYOffset(-4)
        shadow_bot.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow_bot)

        bot_layout = QHBoxLayout(self)
        bot_layout.setContentsMargins(0, 5, 0, 5) 
        bot_layout.setSpacing(0) 

        # Simpan path ikon sebagai variabel kelas agar bisa diakses fungsi lain
        self.icon_home = os.path.join(BASE_DIR, "assets", "icons", "home.svg")
        self.icon_schedule = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        self.icon_history = os.path.join(BASE_DIR, "assets", "icons", "history.svg")
        self.icon_gear = os.path.join(BASE_DIR, "assets", "icons", "gear.svg")

        # Inisialisasi Tombol (Warna diatur di bawah lewat fungsi)
        self.btn_home = QToolButton()
        self.btn_home.setText("Beranda")
        self.btn_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_home.setCursor(Qt.PointingHandCursor)
        self.btn_home.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.btn_home.clicked.connect(self.nav_home.emit)

        self.btn_booking = QToolButton()
        self.btn_booking.setText("Booking")
        self.btn_booking.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_booking.setCursor(Qt.PointingHandCursor)
        self.btn_booking.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_booking.clicked.connect(self.nav_booking.emit)

        self.btn_hist = QToolButton()
        self.btn_hist.setText("Riwayat")
        self.btn_hist.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_hist.setCursor(Qt.PointingHandCursor)
        self.btn_hist.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_hist.clicked.connect(self.nav_history.emit)

        self.btn_settings = QToolButton()
        self.btn_settings.setText("Pengaturan")
        self.btn_settings.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_settings.clicked.connect(self.nav_settings.emit)

        # Masukkan ke layout
        bot_layout.addWidget(self.btn_home)
        bot_layout.addWidget(self.btn_booking)
        bot_layout.addWidget(self.btn_hist)
        bot_layout.addWidget(self.btn_settings)

        # PERUBAHAN: Panggil fungsi pewarnaan saat navbar pertama kali dibuat
        self.set_active_page(active_page)

    # FUNGSI BARU: Mengatur warna berdasarkan halaman yang aktif
    def set_active_page(self, page_name):
        color_active = QColor(34, 197, 94)    # Hijau
        color_inactive = QColor(113, 113, 122) # Abu-abu

        style_active = "color: #22C55E; border: none; font-size: 13px; font-weight: bold;"
        style_inactive = "color: #71717A; border: none; font-size: 13px; font-weight: bold;"

        # 1. Reset semua tombol menjadi abu-abu (tidak aktif)
        self.btn_home.setIcon(create_colored_icon(self.icon_home, color_inactive, 28))
        self.btn_home.setStyleSheet(style_inactive)
        
        self.btn_booking.setIcon(create_colored_icon(self.icon_schedule, color_inactive, 28))
        self.btn_booking.setStyleSheet(style_inactive)
        
        self.btn_hist.setIcon(create_colored_icon(self.icon_history, color_inactive, 28))
        self.btn_hist.setStyleSheet(style_inactive)
        
        self.btn_settings.setIcon(create_colored_icon(self.icon_gear, color_inactive, 28))
        self.btn_settings.setStyleSheet(style_inactive)

        # 2. Beri warna hijau HANYA pada halaman yang sedang dibuka
        if page_name == "beranda":
            self.btn_home.setIcon(create_colored_icon(self.icon_home, color_active, 28))
            self.btn_home.setStyleSheet(style_active)
        elif page_name == "booking":
            self.btn_booking.setIcon(create_colored_icon(self.icon_schedule, color_active, 28))
            self.btn_booking.setStyleSheet(style_active)
        elif page_name == "history":
            self.btn_hist.setIcon(create_colored_icon(self.icon_history, color_active, 28))
            self.btn_hist.setStyleSheet(style_active)
        elif page_name == "pengaturan":
            self.btn_settings.setIcon(create_colored_icon(self.icon_gear, color_active, 28))
            self.btn_settings.setStyleSheet(style_active)