import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, 
                               QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect, QToolButton, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon

from ui.navbar import BottomNavbar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_colored_icon(icon_path, color, size=28):
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

class PengaturanPage(QWidget):
    save_clicked = Signal(str, str, str)  
    logout_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("homePage")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("#homePage { background-color: #F5F5F5; }")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- TOP NAVBAR ---
        self.top_nav = QFrame()
        self.top_nav.setFixedHeight(65)
        self.top_nav.setAttribute(Qt.WA_StyledBackground, True)
        self.top_nav.setStyleSheet("background-color: white;")
        
        shadow_top = QGraphicsDropShadowEffect(self)
        shadow_top.setBlurRadius(15)
        shadow_top.setXOffset(0)
        shadow_top.setYOffset(4)
        shadow_top.setColor(QColor(0, 0, 0, 20))
        self.top_nav.setGraphicsEffect(shadow_top)

        top_layout = QHBoxLayout(self.top_nav)
        top_layout.setContentsMargins(25, 0, 25, 0)

        self.title_top = QLabel("Pengaturan Akun")
        self.title_top.setStyleSheet("font-size: 20px; font-weight: bold; color: #111827;")
        self.title_top.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.title_top)

        # --- SCROLL AREA KONTEN ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background-color: transparent;")
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(25, 25, 25, 25)
        self.scroll_layout.setSpacing(20)

        # --- KARTU FORMULIR (GAYA ADMIN PENGATURAN) ---
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
            QLabel {
                border: none;
                font-size: 14px;
                color: #374151;
                font-weight: 600;
            }
            QLineEdit {
                padding: 12px 15px;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                background-color: #F9FAFB;
                font-size: 14px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #22C55E;
                background-color: #FFFFFF;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        # 1. Input Nama
        lbl_nama = QLabel("Nama Baru:")
        self.inp_nama = QLineEdit()
        self.inp_nama.setPlaceholderText("Masukkan nama baru...")

        # 2. Input Kata Sandi
        lbl_pass = QLabel("Kata Sandi Baru:")
        self.inp_pass = QLineEdit()
        self.inp_pass.setEchoMode(QLineEdit.Password)
        self.inp_pass.setPlaceholderText("Kosongkan jika tidak diganti")

        # 3. Input Konfirmasi Kata Sandi
        lbl_conf = QLabel("Konfirmasi Kata Sandi Baru:")
        self.inp_conf_pass = QLineEdit()
        self.inp_conf_pass.setEchoMode(QLineEdit.Password)
        self.inp_conf_pass.setPlaceholderText("Kosongkan jika tidak diganti")

        # 4. Tombol Simpan
        self.btn_simpan = QPushButton("Simpan Perubahan")
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.setFixedSize(200, 45)
        self.btn_simpan.setStyleSheet("""
            QPushButton {
                background-color: #22C55E;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
        """)
        self.btn_simpan.clicked.connect(self.on_simpan_clicked)

        card_layout.addWidget(lbl_nama)
        card_layout.addWidget(self.inp_nama)
        card_layout.addWidget(lbl_pass)
        card_layout.addWidget(self.inp_pass)
        card_layout.addWidget(lbl_conf)
        card_layout.addWidget(self.inp_conf_pass)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 15, 0, 0)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_simpan)
        
        card_layout.addLayout(btn_layout)
        
        self.scroll_layout.addWidget(card)

        # --- BUTTON KELUAR AKUN ---
        self.btn_logout = QPushButton(" Keluar Akun")
        icon_logout_path = os.path.join(BASE_DIR, "assets", "icons", "logout.svg")
        self.btn_logout.setIcon(create_colored_icon(icon_logout_path, QColor(255, 255, 255), 24))
        self.btn_logout.setIconSize(QSize(24, 24))
        self.btn_logout.setFixedHeight(50)
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #EF4444; 
                color: white; 
                border-radius: 8px; 
                font-size: 15px;
                font-weight: bold; 
                border: none;
            }
            QPushButton:hover { background-color: #DC2626; }
        """)
        
        shadow_logout = QGraphicsDropShadowEffect(self)
        shadow_logout.setBlurRadius(15)
        shadow_logout.setXOffset(0)
        shadow_logout.setYOffset(4)
        shadow_logout.setColor(QColor(0, 0, 0, 15))
        self.btn_logout.setGraphicsEffect(shadow_logout)
        
        self.btn_logout.clicked.connect(lambda: self.logout_clicked.emit())
        self.scroll_layout.addWidget(self.btn_logout)

        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)

        # --- BOTTOM NAVBAR ---
        self.bot_nav = BottomNavbar(active_page="pengaturan")

        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

    def load_data(self, nama_sekarang):
        # Mengisi input nama dengan nama user saat ini
        self.inp_nama.setText(nama_sekarang)
        # Mengosongkan field password agar user tidak bingung
        self.inp_pass.clear()
        self.inp_conf_pass.clear()

    def on_simpan_clicked(self):
        # Ambil nilai saat ini
        nama = self.inp_nama.text().strip()
        pwd = self.inp_pass.text().strip()
        conf_pwd = self.inp_conf_pass.text().strip()

        # Jika nama kosong, kita tidak mengirimkan "" kosong ke database
        # Kita kirimkan indikator bahwa nama tidak berubah
        nama_final = nama if nama != "" else "KEEP_OLD_NAME"

        # Validasi Password (hanya jika diisi)
        if pwd or conf_pwd:
            if len(pwd) < 6:
                QMessageBox.warning(self, "Peringatan", "Password minimal 6 karakter!")
                return
            if pwd != conf_pwd:
                QMessageBox.warning(self, "Peringatan", "Konfirmasi kata sandi tidak cocok!")
                return

        self.save_clicked.emit(nama_final, pwd, conf_pwd)