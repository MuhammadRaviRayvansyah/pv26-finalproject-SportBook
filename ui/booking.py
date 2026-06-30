import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QSizePolicy, 
                             QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath

from ui.navbar import BottomNavbar, create_colored_icon
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CardImage(QWidget):
    def __init__(self, img_path, parent=None):
        super().__init__(parent)
        self.setFixedHeight(240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pixmap = QPixmap(img_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        super().paintEvent(event)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 14, 14)
            painter.setClipPath(path)
            
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.setBrush(QColor("#e5e7eb"))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)

class FieldCard(QFrame):
    request_book = Signal(str, str, int)
    def __init__(self, img_name, title, price_str, parent=None):
        super().__init__(parent)
        self.setObjectName("fieldCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.harga_int = int(price_str.replace(".", ""))
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 45))
        self.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(15) 

        img_path = os.path.join(BASE_DIR, "assets", "images", img_name)
        self.img_widget = CardImage(img_path)
        main_layout.addWidget(self.img_widget)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(8) 
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("cardTitle")
        self.title_lbl.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(self.title_lbl)
        
        loc_layout = QHBoxLayout()
        loc_icon = QLabel()
        icon_loc_path = os.path.join(BASE_DIR, "assets", "icons", "location.svg")
        loc_icon.setPixmap(create_colored_icon(icon_loc_path, QColor("#111827"), 18).pixmap(20, 20))
        loc_icon.setFixedSize(20, 20)
        
        lbl_loc_title = QLabel("Lokasi:")
        lbl_loc_title.setObjectName("lbl")
        lbl_loc_title.setFixedWidth(55)
        lbl_loc = QLabel("Mataram, Jalan Sriwijaya")
        lbl_loc.setObjectName("lbl")

        loc_layout.addWidget(loc_icon)
        loc_layout.addWidget(lbl_loc_title)
        loc_layout.addWidget(lbl_loc)
        info_layout.addLayout(loc_layout)

        buka_layout = QHBoxLayout()
        buka_icon = QLabel()
        icon_buka_path = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        buka_icon.setPixmap(create_colored_icon(icon_buka_path, QColor("#111827"), 18).pixmap(20, 20))
        buka_icon.setFixedSize(20, 20)
        
        lbl_buka = QLabel("Buka:")
        lbl_buka.setObjectName("lbl")
        lbl_buka.setFixedWidth(55)
        lbl_buka_val = QLabel("Senin - Minggu")
        lbl_buka_val.setObjectName("lbl")

        buka_layout.addWidget(buka_icon)
        buka_layout.addWidget(lbl_buka)
        buka_layout.addWidget(lbl_buka_val)
        info_layout.addLayout(buka_layout)

        jam_layout = QHBoxLayout()
        jam_icon = QLabel()
        icon_jam_path = os.path.join(BASE_DIR, "assets", "icons", "time.svg")
        jam_icon.setPixmap(create_colored_icon(icon_jam_path, QColor("#111827"), 18).pixmap(20, 20))
        jam_icon.setFixedSize(20, 20)
        
        lbl_jam = QLabel("Jam:")
        lbl_jam.setObjectName("lbl")
        lbl_jam.setFixedWidth(55)
        lbl_jam_val = QLabel("08.00 - 22.00")
        lbl_jam_val.setObjectName("lbl")

        jam_layout.addWidget(jam_icon)
        jam_layout.addWidget(lbl_jam)
        jam_layout.addWidget(lbl_jam_val)
        info_layout.addLayout(jam_layout)

        main_layout.addLayout(info_layout)

        # Bagian Label Harga, Harga, dan Tombol Booking
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(0)
        
        price_group = QVBoxLayout()
        self.price_tag = QLabel("Harga")
        self.price_tag.setObjectName("priceLabel")
        self.price_val = QLabel(f"{price_str}/Jam")
        self.price_val.setObjectName("cardPrice")

        price_group.addWidget(self.price_tag)
        price_group.addWidget(self.price_val)
        
        self.btn_book = QPushButton("Booking Lapangan")
        self.btn_book.setObjectName("btnCardAction")
        self.btn_book.setFixedSize(150, 42)
        self.btn_book.setCursor(Qt.PointingHandCursor)
        
        self.btn_book.clicked.connect(lambda: self.request_book.emit(title, img_name, self.harga_int))
        
        bottom_layout.addLayout(price_group)
        bottom_layout.addWidget(self.btn_book)

        main_layout.addLayout(bottom_layout)


class BookingPage(QWidget):
    request_book = Signal(str, str, int)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # - JARAK FITUR BOOKING
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # - TOP BAR
        self.top_nav = QFrame()
        self.top_nav.setObjectName("topNav")
        self.top_nav.setFixedHeight(65)
        
        # - DROP SHADOW PADA QFRAME
        shadow_top = QGraphicsDropShadowEffect(self)
        shadow_top.setBlurRadius(15)
        shadow_top.setXOffset(0)
        shadow_top.setYOffset(4)
        shadow_top.setColor(QColor(0, 0, 0, 20))
        self.top_nav.setGraphicsEffect(shadow_top)

        top_layout = QHBoxLayout(self.top_nav)
        top_layout.setContentsMargins(25, 0, 25, 0)

        # - BAGIAN KIRI: LOGO
        self.logo = QLabel()
        pix_logo = QPixmap(os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png"))
        if not pix_logo.isNull():
            self.logo.setPixmap(pix_logo.scaled(130, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # - BAGIAN KANAN: NAMA PROFIL
        user_layout = QHBoxLayout()
        self.user_name = QLabel("Ravi")
        self.user_name.setObjectName("userName")

        # - MEMASUKKAN KOMPONEN WIDGET
        user_layout.addWidget(self.user_name)
        top_layout.addWidget(self.logo)
        top_layout.addStretch()
        top_layout.addLayout(user_layout)

        # - SCROLL AREA
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setObjectName("contentScroll")
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # - SCROLL KONTEN UTAMA
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(25, 25, 25, 25)
        self.scroll_layout.setSpacing(25)

        self.fields_container = QWidget()

        self.fields_layout = QVBoxLayout(self.fields_container)
        self.fields_layout.setContentsMargins(0, 0, 0, 25)
        self.fields_layout.setSpacing(25)

        self.scroll_layout.addWidget(self.fields_container)
        self.scroll.setWidget(self.scroll_content)
        
        # - BOTTOM BAR
        self.bot_nav = BottomNavbar(active_page="booking")

        # - MENAMBAHKAN WIDGET KE MAIN LAYOUT
        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

        # - POSISI TETAP TOPBAR DAN NAVBAR
        self.top_nav.raise_()
        self.bot_nav.raise_()

    def load_dynamic_fields(self, fields):
        # - BERSIHKAN LAYOUT LAMA
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # - TAMBAHKAN CARD LAPANGAN BARU BERDASARKAN DATABASE
        for f in fields:
            card = FieldCard(f[2], f[1], f[3])
            card.request_book.connect(self.request_book.emit)
            self.fields_layout.addWidget(card)