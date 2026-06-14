import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class NotifSuksesPage(QWidget):
    # Signal untuk kembali ke beranda
    back_to_home = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # PERBAIKAN 1 & 2: Mengganti ObjectName dan memaksa warna putih solid (#FFFFFF)
        self.setObjectName("notifSuksesPage")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("QWidget#notifSuksesPage { background-color: #FFFFFF; }")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(0)

        # Spacer Atas agar konten ke tengah vertikal
        self.main_layout.addStretch()

        # 1. Icon Sukses
        self.icon_label = QLabel()
        img_path = os.path.join(BASE_DIR, "assets", "images", "sukses.png")
        pix = QPixmap(img_path)
        if not pix.isNull():
            self.icon_label.setPixmap(pix.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.icon_label)

        self.main_layout.addSpacing(30)

        # 2. Judul Transaksi Berhasil
        self.lbl_title = QLabel("Transaksi\nBerhasil")
        self.lbl_title.setObjectName("notifTitle")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.lbl_title)

        self.main_layout.addSpacing(15)

        # 3. Deskripsi
        self.lbl_desc = QLabel("Selamat Anda Telah\nBerhasil Memesan Lapangan")
        self.lbl_desc.setObjectName("notifDesc")
        self.lbl_desc.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.lbl_desc)

        # Spacer Tengah
        self.main_layout.addStretch()

        # 4. Tombol Kembali
        self.btn_back = QPushButton("Kembali")
        self.btn_back.setObjectName("btnSubmitGreen") 
        self.btn_back.setFixedHeight(55)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(lambda: self.back_to_home.emit())
        self.main_layout.addWidget(self.btn_back)