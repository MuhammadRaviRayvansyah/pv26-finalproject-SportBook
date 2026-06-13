import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect,
                             QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor, QPainter
from database.db_manager import register_user
# Mendapatkan path absolut root project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BackgroundFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Nama file asset tetap menggunakan nama awal: stadium_bg.jpg
        self.bg_path = os.path.join(BASE_DIR, "assets", "images", "stadium_bg.jpg")
        self.pixmap = QPixmap(self.bg_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.fillRect(self.rect(), QColor("#1a1a1a"))

class RegisterPage(QWidget):
    register_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("SportBook - Register")
        self.setMinimumSize(800, 500)
        self.resize(1000, 600)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_frame = BackgroundFrame()
        self.bg_layout = QVBoxLayout(self.bg_frame)
        self.bg_layout.setAlignment(Qt.AlignCenter)

        # --- CARD REGISTER ---
        self.register_card = QFrame()
        self.register_card.setObjectName("authCard")
        self.register_card.setFixedWidth(450)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.register_card.setGraphicsEffect(shadow)

        self.card_layout = QVBoxLayout(self.register_card)
        self.card_layout.setContentsMargins(40, 35, 40, 35)
        self.card_layout.setSpacing(15) 

        # Logo - Nama file asset tetap menggunakan nama awal: sportbook_logo.png
        self.logo_label = QLabel()
        logo_img = os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png")
        pix_logo = QPixmap(logo_img)
        if not pix_logo.isNull():
            self.logo_label.setPixmap(pix_logo.scaledToWidth(150, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(self.logo_label)

        # Header Text
        header_container = QVBoxLayout()
        header_container.setSpacing(2) 
        
        self.title_label = QLabel("Buat Sebuah Akun")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Kata 'Anda' dihapus agar teks muat dalam 1 baris
        self.subtitle_label = QLabel("Masukkan nama, email, dan password untuk membuat akun")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        
        header_container.addWidget(self.title_label)
        header_container.addWidget(self.subtitle_label)
        self.card_layout.addLayout(header_container)
        self.card_layout.addSpacing(5)

        # Field Nama
        nama_group = QVBoxLayout()
        nama_group.setSpacing(5) 
        
        self.nama_label = QLabel("Nama")
        self.nama_label.setObjectName("fieldLabel")
        self.nama_input = QLineEdit()
        self.nama_input.setFixedHeight(42)
        
        nama_group.addWidget(self.nama_label)
        nama_group.addWidget(self.nama_input)
        self.card_layout.addLayout(nama_group)

        # Field Email
        email_group = QVBoxLayout()
        email_group.setSpacing(5) 
        
        self.email_label = QLabel("Email")
        self.email_label.setObjectName("fieldLabel")
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(42)
        
        email_group.addWidget(self.email_label)
        email_group.addWidget(self.email_input)
        self.card_layout.addLayout(email_group)

        # Field Password
        pass_group = QVBoxLayout()
        pass_group.setSpacing(5) 
        
        self.pass_label = QLabel("Password")
        self.pass_label.setObjectName("fieldLabel")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("••••••••")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(42)
        
        pass_group.addWidget(self.pass_label)
        pass_group.addWidget(self.pass_input)
        self.card_layout.addLayout(pass_group)
        self.card_layout.addSpacing(5)

        # Button Daftar
        self.btn_submit = QPushButton("Daftar")
        self.btn_submit.setObjectName("btnSubmit")
        self.btn_submit.setFixedHeight(48)
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        self.card_layout.addWidget(self.btn_submit)
        # Hubungkan tombol daftar ke fungsi proses_pendaftaran
        self.btn_submit.clicked.connect(self.proses_pendaftaran)

        # Footer
        footer_box = QHBoxLayout()
        self.f_text = QLabel("Sudah Punya Akun?")
        self.f_text.setObjectName("footerText")
        self.f_link = QPushButton("Masuk Sekarang.")
        self.f_link.setObjectName("footerLink")
        self.f_link.setCursor(Qt.PointingHandCursor)
        
        footer_box.addStretch()
        footer_box.addWidget(self.f_text)
        footer_box.addWidget(self.f_link)
        footer_box.addStretch()
        self.card_layout.addLayout(footer_box)

        self.bg_layout.addWidget(self.register_card)
        self.main_layout.addWidget(self.bg_frame)

    # --- FUNGSI LOGIKA DATABASE ---
    def proses_pendaftaran(self):
        nama = self.nama_input.text().strip()
        email = self.email_input.text().strip()
        password = self.pass_input.text().strip()

        # Validasi Kosong
        if not nama or not email or not password:
            QMessageBox.warning(self, "Peringatan", "Semua kolom wajib diisi!")
            return

        # Memanggil fungsi dari db_manager
        sukses, pesan = register_user(nama, email, password)

        if sukses:
            QMessageBox.information(self, "Berhasil", pesan)
            self.nama_input.clear()
            self.email_input.clear()
            self.pass_input.clear()
            self.register_successful.emit()
        else:
            QMessageBox.critical(self, "Gagal", pesan)