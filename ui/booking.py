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
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(8) 
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("cardTitle")
        self.title_lbl.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(self.title_lbl)
        
        loc_layout = QHBoxLayout()
        loc_layout.setContentsMargins(0, 0, 0, 0)
        loc_layout.setSpacing(8)
        loc_icon = QLabel()
        icon_loc_path = os.path.join(BASE_DIR, "assets", "icons", "location.svg")
        loc_icon.setPixmap(create_colored_icon(icon_loc_path, QColor("#111827"), 18).pixmap(20, 20))
        loc_icon.setFixedSize(20, 20)
        loc_icon.setAlignment(Qt.AlignCenter)
        
        lbl_loc_title = QLabel("Lokasi:")
        lbl_loc_title.setStyleSheet("color: #000000; font-weight: bold;")
        lbl_loc_title.setFixedWidth(55)
        lbl_loc = QLabel("Mataram, Jalan xxxx")
        lbl_loc.setStyleSheet("color: #000000; font-weight: bold;")
        loc_layout.addWidget(loc_icon)
        loc_layout.addWidget(lbl_loc_title)
        loc_layout.addWidget(lbl_loc)
        loc_layout.addStretch()
        info_layout.addLayout(loc_layout)

        buka_layout = QHBoxLayout()
        buka_layout.setContentsMargins(0, 0, 0, 0)
        buka_layout.setSpacing(8)
        buka_icon = QLabel()
        icon_buka_path = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        buka_icon.setPixmap(create_colored_icon(icon_buka_path, QColor("#111827"), 18).pixmap(20, 20))
        buka_icon.setFixedSize(20, 20)
        buka_icon.setAlignment(Qt.AlignCenter)
        
        lbl_buka = QLabel("Buka:")
        lbl_buka.setStyleSheet("color: #000000; font-weight: bold;")
        lbl_buka.setFixedWidth(55)
        lbl_buka_val = QLabel("Senin - Minggu")
        lbl_buka_val.setStyleSheet("color: #000000; font-weight: bold;")
        buka_layout.addWidget(buka_icon)
        buka_layout.addWidget(lbl_buka)
        buka_layout.addWidget(lbl_buka_val)
        buka_layout.addStretch()
        info_layout.addLayout(buka_layout)

        jam_layout = QHBoxLayout()
        jam_layout.setContentsMargins(0, 0, 0, 0)
        jam_layout.setSpacing(8)
        jam_icon = QLabel()
        icon_jam_path = os.path.join(BASE_DIR, "assets", "icons", "time.svg")
        jam_icon.setPixmap(create_colored_icon(icon_jam_path, QColor("#111827"), 18).pixmap(20, 20))
        jam_icon.setFixedSize(20, 20)
        jam_icon.setAlignment(Qt.AlignCenter)
        
        lbl_jam = QLabel("Jam:")
        lbl_jam.setStyleSheet("color: #000000; font-weight: bold;")
        lbl_jam.setFixedWidth(55)
        lbl_jam_val = QLabel("08.00 - 22.00")
        lbl_jam_val.setStyleSheet("color: #000000; font-weight: bold;")
        jam_layout.addWidget(jam_icon)
        jam_layout.addWidget(lbl_jam)
        jam_layout.addWidget(lbl_jam_val)
        jam_layout.addStretch()
        info_layout.addLayout(jam_layout)

        main_layout.addLayout(info_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        
        price_group = QVBoxLayout()
        price_group.setContentsMargins(0, 0, 0, 0)
        price_group.setSpacing(0)
        self.price_tag = QLabel("Harga")
        self.price_tag.setObjectName("priceLabel")
        self.price_tag.setContentsMargins(0, 0, 0, 0)
        self.price_tag.setStyleSheet("color: #000000; font-weight: bold;")
        self.price_val = QLabel(f"{price_str}/Jam")
        self.price_val.setObjectName("cardPrice")
        self.price_val.setContentsMargins(0, 0, 0, 0)
        price_group.addWidget(self.price_tag)
        price_group.addWidget(self.price_val)
        
        self.btn_book = QPushButton("Booking Lapangan")
        self.btn_book.setObjectName("btnCardAction")
        self.btn_book.setFixedSize(150, 42)
        self.btn_book.setCursor(Qt.PointingHandCursor)
        
        self.btn_book.clicked.connect(lambda: self.request_book.emit(title, img_name, self.harga_int))
        
        bottom_layout.addLayout(price_group)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_book)

        main_layout.addLayout(bottom_layout)


class BookingPage(QWidget):
    request_book = Signal(str, str, int)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("homePage")
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
        
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.btn_back)
        left_layout.addStretch()

        self.title_top = QLabel("Booking Lapangan")
        self.title_top.setObjectName("topTitle")
        self.title_top.setAlignment(Qt.AlignCenter)

        user_layout = QHBoxLayout()
        user_layout.setSpacing(12)
        self.user_name = QLabel("Ravi")
        self.user_name.setObjectName("userName")
        
        self.icon_user = QLabel()
        user_icon_path = os.path.join(BASE_DIR, "assets", "icons", "user.svg")
        user_pixmap = QPixmap(user_icon_path)
        if not user_pixmap.isNull():
            self.icon_user.setPixmap(user_pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_user.setFixedSize(22, 22)

        user_layout.addWidget(self.user_name)
        user_layout.addWidget(self.icon_user)

        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addStretch()
        right_layout.addLayout(user_layout)

        top_layout.addWidget(left_container, 1)
        top_layout.addWidget(self.title_top, 2)
        top_layout.addWidget(right_container, 1)

        # --- SCROLL AREA ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setObjectName("contentScroll")
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        # --- KONTEN UTAMA ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)
        
        # Container untuk kartu lapangan dinamis
        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_container)
        self.fields_layout.setContentsMargins(0, 0, 0, 25)
        self.fields_layout.setSpacing(25)
        content_layout.addWidget(self.fields_container)

        self.scroll_layout.addWidget(content_widget)
        self.scroll.setWidget(self.scroll_content)
        
        # --- BOTTOM NAVBAR ---
        self.bot_nav = BottomNavbar(active_page="booking")

        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

        self.top_nav.raise_()
        self.bot_nav.raise_()

    def load_dynamic_fields(self, fields):
        # Bersihkan layout lama
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Tambahkan kartu baru berdasarkan database
        for f in fields:
            # f: (id, nama, gambar, harga, deskripsi, kategori)
            card = FieldCard(f[2], f[1], f[3])
            card.request_book.connect(self.request_book.emit)
            self.fields_layout.addWidget(card)