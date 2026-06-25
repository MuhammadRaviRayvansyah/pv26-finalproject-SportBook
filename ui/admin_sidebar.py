import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QFrame, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QColor, QPainter, QIcon

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_colored_icon(icon_path, color, size=24):
    pixmap = QPixmap(icon_path)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        painter = QPainter(colored_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), color)
        painter.end()
        return QIcon(colored_pixmap)
    return QIcon()

class AdminSidebar(QFrame):
    # Memperbarui daftar signal yang dipancarkan
    nav_changed = Signal(str) # "dashboard", "bookings", "settings", "logout"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setObjectName("adminSidebar")
        self.setStyleSheet("""
            #adminSidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
            }
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                color: #4B5563;
                background: transparent;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
                color: #111827;
            }
            QPushButton#activeNav {
                background-color: #F0FDF4;
                color: #16A34A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 30, 15, 20)
        layout.setSpacing(8)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png")
        pixmap_logo = QPixmap(logo_path)
        if not pixmap_logo.isNull():
            logo_label.setPixmap(pixmap_logo.scaled(160, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setContentsMargins(0, 0, 0, 30)
        layout.addWidget(logo_label)

        # Menu Buttons (Telah Disesuaikan)
        self.btn_dashboard = self._create_nav_btn("Dashboard", "home.svg", "dashboard")
        self.btn_bookings = self._create_nav_btn("Daftar Pesanan", "history.svg", "bookings")
        self.btn_settings = self._create_nav_btn("Pengaturan", "gear.svg", "settings")
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_bookings)
        layout.addWidget(self.btn_settings)
        
        layout.addStretch()

        # Logout Button
        self.btn_logout = self._create_nav_btn("Keluar", "logout.svg", "logout", is_logout=True)
        layout.addWidget(self.btn_logout)

        # Memperbarui daftar tombol aktif
        self.buttons = [self.btn_dashboard, self.btn_bookings, self.btn_settings]
        
        # Panggilan ini akan mengatur warna ikon Dashboard menjadi hijau saat aplikasi pertama kali dimuat
        self.set_active("dashboard")

    def _create_nav_btn(self, text, icon_name, nav_target, is_logout=False):
        btn = QPushButton(f"  {text}")
        
        # Warna ikon default diatur di sini (akan ditimpa secara dinamis oleh set_active nantinya)
        icon_path = os.path.join(BASE_DIR, "assets", "icons", icon_name)
        color = QColor("#EF4444") if is_logout else QColor("#4B5563")
        btn.setIcon(create_colored_icon(icon_path, color, 20))
        btn.setIconSize(QSize(20, 20))
        btn.setCursor(Qt.PointingHandCursor)
        
        if is_logout:
            btn.setStyleSheet("color: #EF4444; font-weight: bold;")
            btn.clicked.connect(lambda: self.nav_changed.emit("logout"))
        else:
            btn.clicked.connect(lambda: self._handle_click(btn, nav_target))
        
        return btn

    def _handle_click(self, btn, target):
        self.set_active(target)
        self.nav_changed.emit(target)

    def set_active(self, target):
        # 1. Bersihkan state aktif sebelumnya
        for b in self.buttons:
            b.setObjectName("")
        
        # 2. Tentukan tombol mana yang sedang aktif
        active_btn = None
        if target == "dashboard": active_btn = self.btn_dashboard
        elif target == "bookings": active_btn = self.btn_bookings
        elif target == "settings": active_btn = self.btn_settings
        
        if active_btn:
            active_btn.setObjectName("activeNav")
        
        # --- PERBAIKAN: PEWARNAAN IKON DINAMIS ---
        
        warna_aktif = QColor("#16A34A")  
        warna_biasa = QColor("#4B5563")  
        
        # Update ikon Dashboard
        path_dash = os.path.join(BASE_DIR, "assets", "icons", "home.svg")
        self.btn_dashboard.setIcon(create_colored_icon(path_dash, warna_aktif if target == "dashboard" else warna_biasa, 20))
        
        # Update ikon Daftar Pesanan
        path_book = os.path.join(BASE_DIR, "assets", "icons", "history.svg")
        self.btn_bookings.setIcon(create_colored_icon(path_book, warna_aktif if target == "bookings" else warna_biasa, 20))
        
        # Update ikon Pengaturan
        path_settings = os.path.join(BASE_DIR, "assets", "icons", "gear.svg")
        self.btn_settings.setIcon(create_colored_icon(path_settings, warna_aktif if target == "settings" else warna_biasa, 20))
        
        # Refresh stylesheet agar perubahan objectName segera diterapkan
        self.setStyleSheet(self.styleSheet())