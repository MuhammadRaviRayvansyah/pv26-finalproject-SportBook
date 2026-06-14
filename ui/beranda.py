import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QSizePolicy, 
                             QGraphicsDropShadowEffect, QToolButton)
from PySide6.QtCore import Qt, QSize, Signal
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

class HeroFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("heroSection")
        self.setFixedHeight(320)
        self.bg_path = os.path.join(BASE_DIR, "assets", "images", "stadium_bg.jpg")
        self.pixmap = QPixmap(self.bg_path)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 45))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 24, 24)
            painter.setClipPath(path)
            
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.setBrush(QColor("#e5e7eb"))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 24, 24)

class CardImage(QWidget):
    def __init__(self, img_path, parent=None):
        super().__init__(parent)
        self.setFixedHeight(240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pixmap = QPixmap(img_path)

    def paintEvent(self, event):
        painter = QPainter(self)
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
        self.price_tag.setObjectName("cardDesc")
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


class HomePage(QWidget):
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

        self.logo = QLabel()
        pix_logo = QPixmap(os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png"))
        if not pix_logo.isNull():
            self.logo.setPixmap(pix_logo.scaled(130, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
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
        self.icon_user.setCursor(Qt.PointingHandCursor)

        # Ikon lonceng dihapus dari sini
        
        user_layout.addWidget(self.user_name)
        user_layout.addWidget(self.icon_user)

        top_layout.addWidget(self.logo)
        top_layout.addStretch()
        top_layout.addLayout(user_layout)

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

        # --- KONTEN (HERO + FIELD CARDS) ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)

        self.hero = HeroFrame()
        hero_layout = QVBoxLayout(self.hero)
        hero_layout.setContentsMargins(35, 30, 35, 30)
        hero_layout.setSpacing(12)
        
        self.h_title = QLabel("Hallo, <b style='color:#22C55E;'>Pengguna!</b>")
        self.h_title.setObjectName("heroTitle")

        self.h_sub1 = QLabel("Booking futsal hari ini?")
        self.h_sub1.setObjectName("heroSub")
        self.h_sub1.setContentsMargins(0, 5, 0, 0)

        self.h_sub2 = QLabel("Terdapat pilihan lapangan dan jam booking")
        self.h_sub2.setObjectName("heroSub")
        self.h_sub2.setContentsMargins(0, 0, 0, 10)
        
        self.loc_badge = QPushButton(" Lokasi: Mataram, Jalan xxxx")
        self.loc_badge.setObjectName("locBadge")
        self.loc_badge.setFixedSize(220, 42)
        self.loc_badge.setCursor(Qt.PointingHandCursor)
        self.loc_badge.setContentsMargins(0, 5, 0, 5)
        
        icon_loc_path = os.path.join(BASE_DIR, "assets", "icons", "location.svg")
        self.loc_badge.setIcon(create_colored_icon(icon_loc_path, QColor(255, 255, 255), 18))
        self.loc_badge.setIconSize(QSize(18, 18))
        
        self.btn_hero = QPushButton("Booking Sekarang")
        self.btn_hero.setObjectName("btnHero")
        self.btn_hero.setFixedSize(220, 42)
        self.btn_hero.setCursor(Qt.PointingHandCursor)
        self.btn_hero.setContentsMargins(0, 10, 0, 0)

        hero_layout.addWidget(self.h_title)
        hero_layout.addWidget(self.h_sub1)
        hero_layout.addWidget(self.h_sub2)
        hero_layout.addStretch() 
        hero_layout.addWidget(self.loc_badge)
        hero_layout.addWidget(self.btn_hero)
        
        content_layout.addWidget(self.hero)
        
        self.list_title = QLabel("List Lapangan")
        self.list_title.setObjectName("sectionTitle")
        self.list_title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.list_title)

        card1 = FieldCard("lapangan_1.jpg", "Lapangan 1", "200.000")
        card1.request_book.connect(self.request_book.emit)
        content_layout.addWidget(card1)

        card2 = FieldCard("lapangan_2.jpg", "Lapangan 2", "200.000")
        card2.request_book.connect(self.request_book.emit)
        content_layout.addWidget(card2)

        card3 = FieldCard("lapangan_3.jpg", "Lapangan 3", "200.000")
        card3.request_book.connect(self.request_book.emit)
        content_layout.addWidget(card3)

        self.scroll_layout.addWidget(content_widget)
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

        # AKTIF: HIJAU
        self.btn_home = QToolButton()
        self.btn_home.setIcon(create_colored_icon(icon_home, QColor(34, 197, 94), 28)) 
        self.btn_home.setText("Beranda")
        self.btn_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_home.setCursor(Qt.PointingHandCursor)
        self.btn_home.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.btn_home.setStyleSheet("color: #22C55E; border: none; font-size: 13px; font-weight: bold;")

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

        self.btn_settings = QToolButton()
        self.btn_settings.setIcon(create_colored_icon(icon_gear, QColor(113, 113, 122), 28)) 
        self.btn_settings.setText("Pengaturan")
        self.btn_settings.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_settings.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        bot_layout.addWidget(self.btn_home)
        bot_layout.addWidget(self.btn_booking)
        bot_layout.addWidget(self.btn_hist)
        bot_layout.addWidget(self.btn_settings)

        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

        self.top_nav.raise_()
        self.bot_nav.raise_()

        self.btn_hero.clicked.connect(self.btn_booking.click)