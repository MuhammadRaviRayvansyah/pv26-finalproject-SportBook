import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect, 
                             QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PaymentOption(QFrame):
    """Komponen Card untuk setiap opsi pembayaran."""
    def __init__(self, logo_filename, nama_metode, logo_w, logo_h, parent=None):
        super().__init__(parent)
        self.setObjectName("paymentCard")
        self.setFixedHeight(80)
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QFrame#paymentCard {
                background-color: white;
                border-radius: 15px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 12px;
                border: 2px solid #111827;
                background-color: white;
                margin: 0px;
            }
            QRadioButton::indicator:checked {
                width: 20px;
                height: 20px;
                border-radius: 12px;
                border: 2px solid #111827;
                background-color: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, 
                    stop:0 #111827, stop:0.45 #111827, 
                    stop:0.55 white, stop:1 white
                );
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        # Logo
        self.logo = QLabel()
        logo_path = os.path.join(BASE_DIR, "assets", "logos", logo_filename)
        pix = QPixmap(logo_path)
        if not pix.isNull():
            self.logo.setPixmap(pix.scaled(logo_w, logo_h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # PERBAIKAN: Membesarkan wadah menjadi 90x60 agar logo GOPAY yang membesar muat di dalamnya
        self.logo.setFixedSize(90, 60)
        self.logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo)

        # Teks Metode
        self.lbl_nama = QLabel(nama_metode)
        self.lbl_nama.setObjectName("paymentTitle")
        layout.addWidget(self.lbl_nama)

        layout.addStretch()

        # Radio Button
        self.radio_btn = QRadioButton()
        self.radio_btn.setObjectName("paymentRadio")
        self.radio_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.radio_btn)

class PembayaranPage(QWidget):
    confirm_payment = Signal(str) 
    go_back = Signal()

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
        self.top_nav.setObjectName("topNav")
        self.top_nav.setFixedHeight(65)
        
        shadow_top = QGraphicsDropShadowEffect(self)
        shadow_top.setBlurRadius(15)
        shadow_top.setXOffset(0)
        shadow_top.setYOffset(4)
        shadow_top.setColor(QColor(0, 0, 0, 20))
        self.top_nav.setGraphicsEffect(shadow_top)

        top_layout = QHBoxLayout(self.top_nav)
        top_layout.setContentsMargins(25, 0, 25, 0)

        self.btn_back = QPushButton("<")
        self.btn_back.setObjectName("btnBack")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(lambda: self.go_back.emit())
        
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.btn_back)
        left_layout.addStretch()

        self.title_top = QLabel("Pembayaran")
        self.title_top.setObjectName("topTitle")
        self.title_top.setAlignment(Qt.AlignCenter)

        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addStretch() 

        top_layout.addWidget(left_container, 1)
        top_layout.addWidget(self.title_top, 2)
        top_layout.addWidget(right_container, 1)

        self.main_layout.addWidget(self.top_nav)

        # --- SCROLL AREA ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setObjectName("contentScroll")
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.scroll_content.setStyleSheet("#scrollContent { background-color: transparent; }")
        
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(25, 25, 25, 25)
        self.scroll_layout.setSpacing(20)

        # Opsi Pembayaran 
        self.payment_group = QButtonGroup(self)
        
        # PERBAIKAN 1: Parameter height untuk GOPAY diperbesar (dari 45 menjadi 55) agar logonya lebih besar
        self.opt_gopay = PaymentOption("gopay.png", "GOPAY", 115, 85)
        self.payment_group.addButton(self.opt_gopay.radio_btn, 1)
        self.scroll_layout.addWidget(self.opt_gopay)

        self.opt_dana = PaymentOption("dana.png", "DANA", 85, 45)
        self.payment_group.addButton(self.opt_dana.radio_btn, 2)
        self.scroll_layout.addWidget(self.opt_dana)

        self.opt_ovo = PaymentOption("ovo.jpg", "OVO", 45, 45)
        self.payment_group.addButton(self.opt_ovo.radio_btn, 3)
        self.scroll_layout.addWidget(self.opt_ovo)

        self.opt_gopay.radio_btn.setChecked(True)

        # --- CARD SUMMARY (Bagan Durasi & Total) ---
        self.card_summary = QFrame()
        self.card_summary.setObjectName("detailCard")
        
        self.card_summary.setAttribute(Qt.WA_StyledBackground, True)
        self.card_summary.setStyleSheet("QFrame#detailCard { background-color: white; border-radius: 15px; }")

        shadow_sum = QGraphicsDropShadowEffect(self)
        shadow_sum.setBlurRadius(20)
        shadow_sum.setXOffset(0)
        shadow_sum.setYOffset(6)
        shadow_sum.setColor(QColor(0, 0, 0, 20))
        self.card_summary.setGraphicsEffect(shadow_sum)

        summary_layout = QVBoxLayout(self.card_summary)
        summary_layout.setContentsMargins(25, 25, 25, 25)
        summary_layout.setSpacing(25)

        # Baris Durasi
        row_durasi = QHBoxLayout()
        row_durasi.addWidget(QLabel("Durasi", objectName="summaryLabel"))
        row_durasi.addStretch()
        self.lbl_durasi = QLabel("0 JAM")
        self.lbl_durasi.setObjectName("durasiBadge")
        row_durasi.addWidget(self.lbl_durasi)
        summary_layout.addLayout(row_durasi)

        # Baris Total Pembayaran
        row_total = QHBoxLayout()
        row_total.addWidget(QLabel("Total Pembayaran", objectName="summaryLabel"))
        row_total.addStretch()
        self.lbl_total = QLabel("Rp0")
        self.lbl_total.setObjectName("summaryTotal")
        row_total.addWidget(self.lbl_total)
        summary_layout.addLayout(row_total)

        self.scroll_layout.addWidget(self.card_summary)

        # --- TOMBOL BAYAR ---
        self.btn_bayar = QPushButton("Bayar")
        self.btn_bayar.setObjectName("btnSubmitGreen")
        self.btn_bayar.setFixedHeight(50)
        self.btn_bayar.setCursor(Qt.PointingHandCursor)
        self.btn_bayar.clicked.connect(self.on_bayar_clicked)
        self.scroll_layout.addWidget(self.btn_bayar)

        self.scroll_layout.addStretch()

        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        self.top_nav.raise_()

    def load_data(self, jumlah_jam, total_harga):
        self.lbl_durasi.setText(f"{jumlah_jam} JAM")
        
        harga_str = f"{total_harga:,.0f}".replace(",", ".")
        self.lbl_total.setText(f"Rp{harga_str}")

    def on_bayar_clicked(self):
        metode_terpilih = "GOPAY"
        if self.opt_dana.radio_btn.isChecked():
            metode_terpilih = "DANA"
        elif self.opt_ovo.radio_btn.isChecked():
            metode_terpilih = "OVO"
            
        self.confirm_payment.emit(metode_terpilih)