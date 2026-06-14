import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect, QToolButton, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath, QIcon

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

    def create_input_card(self, label_text, is_password=False, placeholder=""):
        card = QFrame()
        card.setFixedHeight(65)
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        card.setGraphicsEffect(shadow)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-size: 16px; color: black;")
        lbl.setFixedWidth(180)

        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setStyleSheet("background: transparent; border: none; font-size: 16px; color: black;")
        if is_password:
            inp.setEchoMode(QLineEdit.Password)

        layout.addWidget(lbl)
        layout.addWidget(inp)
        return card, inp

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
        shadow_top.setBlurRadius(20)
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

        # FORM INPUT
        card_nama, self.inp_nama = self.create_input_card("Nama Baru:", placeholder="Masukkan nama baru...")
        card_pass, self.inp_pass = self.create_input_card("Kata Sandi Baru:", True, placeholder="Kosongkan jika tidak diganti")
        card_conf, self.inp_conf_pass = self.create_input_card("Konfirmasi Kata Sandi Baru:", True, placeholder="Kosongkan jika tidak diganti")

        self.scroll_layout.addWidget(card_nama)
        self.scroll_layout.addWidget(card_pass)
        self.scroll_layout.addWidget(card_conf)

        self.scroll_layout.addSpacing(10)

        # BUTTON SIMPAN
        self.btn_simpan = QPushButton("Simpan")
        self.btn_simpan.setFixedHeight(55)
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.setStyleSheet("""
            QPushButton {
                background-color: #22C55E; 
                color: white; 
                border-radius: 15px; 
                font-size: 16px; 
            }
            QPushButton:hover { background-color: #16a34a; }
        """)
        shadow_btn = QGraphicsDropShadowEffect(self)
        shadow_btn.setBlurRadius(15)
        shadow_btn.setXOffset(0)
        shadow_btn.setYOffset(4)
        shadow_btn.setColor(QColor(0, 0, 0, 20))
        self.btn_simpan.setGraphicsEffect(shadow_btn)
        self.btn_simpan.clicked.connect(self.on_simpan_clicked)
        self.scroll_layout.addWidget(self.btn_simpan)

        # BUTTON KELUAR AKUN
        self.btn_logout = QPushButton(" Keluar Akun")
        icon_logout_path = os.path.join(BASE_DIR, "assets", "icons", "logout.svg")
        self.btn_logout.setIcon(create_colored_icon(icon_logout_path, QColor(255, 255, 255), 24))
        self.btn_logout.setIconSize(QSize(24, 24))
        self.btn_logout.setFixedHeight(55)
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #FF0000; 
                color: white; 
                border-radius: 15px; 
                font-size: 16px; 
            }
            QPushButton:hover { background-color: #DC2626; }
        """)
        shadow_logout = QGraphicsDropShadowEffect(self)
        shadow_logout.setBlurRadius(15)
        shadow_logout.setXOffset(0)
        shadow_logout.setYOffset(4)
        shadow_logout.setColor(QColor(0, 0, 0, 20))
        self.btn_logout.setGraphicsEffect(shadow_logout)
        self.btn_logout.clicked.connect(lambda: self.logout_clicked.emit())
        self.scroll_layout.addWidget(self.btn_logout)

        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)

        # --- BOTTOM NAVBAR ---
        self.bot_nav = QFrame()
        self.bot_nav.setFixedHeight(75)
        self.bot_nav.setAttribute(Qt.WA_StyledBackground, True)
        self.bot_nav.setStyleSheet("background-color: white;")
        
        shadow_bot = QGraphicsDropShadowEffect(self)
        shadow_bot.setBlurRadius(20)
        shadow_bot.setXOffset(0)
        shadow_bot.setYOffset(-4)
        shadow_bot.setColor(QColor(0, 0, 0, 20))
        self.bot_nav.setGraphicsEffect(shadow_bot)

        bot_layout = QHBoxLayout(self.bot_nav)
        bot_layout.setContentsMargins(0, 5, 0, 5) 
        bot_layout.setSpacing(0) 

        icon_home = os.path.join(BASE_DIR, "assets", "icons", "home.svg")
        icon_schedule = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        icon_history = os.path.join(BASE_DIR, "assets", "icons", "history.svg")
        icon_gear = os.path.join(BASE_DIR, "assets", "icons", "gear.svg")

        self.btn_home = QToolButton()
        self.btn_home.setIcon(create_colored_icon(icon_home, QColor(113, 113, 122), 28)) 
        self.btn_home.setText("Beranda")
        self.btn_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_home.setCursor(Qt.PointingHandCursor)
        self.btn_home.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.btn_home.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        self.btn_booking = QToolButton()
        self.btn_booking.setIcon(create_colored_icon(icon_schedule, QColor(113, 113, 122), 28)) 
        self.btn_booking.setText("Booking")
        self.btn_booking.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_booking.setCursor(Qt.PointingHandCursor)
        self.btn_booking.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_booking.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        self.btn_hist = QToolButton()
        self.btn_hist.setIcon(create_colored_icon(icon_history, QColor(113, 113, 122), 28)) 
        self.btn_hist.setText("Riwayat")
        self.btn_hist.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_hist.setCursor(Qt.PointingHandCursor)
        self.btn_hist.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_hist.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        # AKTIF: HIJAU
        self.btn_settings = QToolButton()
        self.btn_settings.setIcon(create_colored_icon(icon_gear, QColor(34, 197, 94), 28)) 
        self.btn_settings.setText("Pengaturan")
        self.btn_settings.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_settings.setStyleSheet("color: #22C55E; border: none; font-size: 13px; font-weight: bold;")

        bot_layout.addWidget(self.btn_home)
        bot_layout.addWidget(self.btn_booking)
        bot_layout.addWidget(self.btn_hist)
        bot_layout.addWidget(self.btn_settings)

        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

    def on_simpan_clicked(self):
        self.save_clicked.emit(self.inp_nama.text(), self.inp_pass.text(), self.inp_conf_pass.text())