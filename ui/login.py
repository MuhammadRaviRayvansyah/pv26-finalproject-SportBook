import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect,
                             QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPainter

# Mendapatkan direktori root proyek secara absolut
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BackgroundFrame(QFrame):
    """Custom QFrame untuk menggambar background image agar selalu responsif dan tampil."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bg_image_path = os.path.join(BASE_DIR, "assets", "images", "stadium_bg.jpg")
        self.pixmap = QPixmap(self.bg_image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Jika gambar ditemukan, gambar sebagai background
        if not self.pixmap.isNull():
            # Skalakan gambar memenuhi layar sambil mempertahankan aspek rasio
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # Posisikan gambar di tengah
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            # Fallback warna jika gambar gagal dimuat
            painter.fillRect(self.rect(), QColor("#1a1a1a"))
        
        super().paintEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("SportBook - Login")
        self.setMinimumSize(800, 500)
        self.resize(1000, 600)
        self.setMaximumSize(1600, 900)

    def setup_ui(self):
        # Layout Utama
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Background Container menggunakan Custom Frame
        self.bg_frame = BackgroundFrame()
        self.bg_frame.setObjectName("bgFrame")
        self.bg_layout = QVBoxLayout(self.bg_frame)
        self.bg_layout.setAlignment(Qt.AlignCenter)

        # --- LOGIN CARD ---
        self.login_card = QFrame()
        self.login_card.setObjectName("loginCard")
        self.login_card.setFixedWidth(450)
        self.login_card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Efek Shadow pada Card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.login_card.setGraphicsEffect(shadow)

        self.card_layout = QVBoxLayout(self.login_card)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20) # Jarak antar grup besar

        # 1. Logo
        self.logo_label = QLabel()
        logo_path = os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png")
        pixmap_logo = QPixmap(logo_path)
        
        if not pixmap_logo.isNull():
            # Atur ukuran logo agar proporsional
            self.logo_label.setPixmap(pixmap_logo.scaled(180, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("[ Logo Tidak Ditemukan ]")
            
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(self.logo_label)

        # 2. Title & Subtitle Group
        self.header_layout = QVBoxLayout()
        self.header_layout.setSpacing(5)
        
        self.title_label = QLabel("Selamat Datang Kembali")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.subtitle_label = QLabel("Masukkan email dan password untuk akses akun Anda")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.subtitle_label)
        self.card_layout.addLayout(self.header_layout)

        # 3. Form Input Email (Diperbaiki jaraknya)
        self.email_layout = QVBoxLayout()
        self.email_layout.setSpacing(8) # Jarak rapat antara label dan input
        
        self.email_label = QLabel("Email")
        self.email_label.setObjectName("fieldLabel")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Masukkan email Anda")
        self.email_input.setFixedHeight(45)

        self.email_layout.addWidget(self.email_label)
        self.email_layout.addWidget(self.email_input)
        self.card_layout.addLayout(self.email_layout)

        # 4. Form Input Password (Diperbaiki jaraknya)
        self.pass_layout = QVBoxLayout()
        self.pass_layout.setSpacing(8) # Jarak rapat antara label dan input
        
        self.pass_label = QLabel("Password")
        self.pass_label.setObjectName("fieldLabel")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("••••••••")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(45)

        self.pass_layout.addWidget(self.pass_label)
        self.pass_layout.addWidget(self.pass_input)
        self.card_layout.addLayout(self.pass_layout)

        # 5. Tombol Masuk
        self.btn_masuk = QPushButton("Masuk")
        self.btn_masuk.setObjectName("btnMasuk")
        self.btn_masuk.setFixedHeight(50)
        self.btn_masuk.setCursor(Qt.PointingHandCursor)
        self.card_layout.addWidget(self.btn_masuk)

        # 6. Footer Text
        self.footer_layout = QHBoxLayout()
        self.footer_text = QLabel("Tidak Punya Akun?")
        self.footer_text.setObjectName("footerText")
        self.footer_link = QPushButton("Daftar Sekarang.")
        self.footer_link.setObjectName("footerLink")
        self.footer_link.setCursor(Qt.PointingHandCursor)
        
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.footer_text)
        self.footer_layout.addWidget(self.footer_link)
        self.footer_layout.addStretch()
        
        self.card_layout.addLayout(self.footer_layout)

        # Pasang Card ke Background
        self.bg_layout.addWidget(self.login_card)
        self.main_layout.addWidget(self.bg_frame)