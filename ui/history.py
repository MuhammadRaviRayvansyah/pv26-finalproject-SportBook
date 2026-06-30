import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath

from ui.navbar import BottomNavbar, create_colored_icon
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class HistoryCard(QFrame):
    delete_clicked = Signal(str, str)

    def __init__(self, lapangan_nama, jam_range, tanggal_booking, parent=None):
        super().__init__(parent)
        self.setObjectName("historyCard")
        self.setFixedHeight(200) 
        
        img_map = {
            "Lapangan 1": "lapangan_1.jpg",
            "Lapangan 2": "lapangan_2.jpg",
            "Lapangan 3": "lapangan_3.jpg"
        }
        img_name = img_map.get(lapangan_nama, "lapangan_1.jpg")
        img_path = os.path.join(BASE_DIR, "assets", "images", img_name)

        self.setAttribute(Qt.WA_StyledBackground, True)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # GAMBAR LAPANGAN
        self.img_label = QLabel()
        self.img_label.setFixedSize(170, 150)

        pix = QPixmap(img_path)

        if not pix.isNull():
            scaled = pix.scaled(170, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

            path = QPainterPath()
            path.addRoundedRect(0, 0, 170, 150, 15, 15)
            
            canvas = QPixmap(170, 150)
            canvas.fill(Qt.transparent)

            painter = QPainter(canvas)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled)
            painter.end()

            self.img_label.setPixmap(canvas)

        self.img_label.setAlignment(Qt.AlignTop)
        
        img_layout = QVBoxLayout()
        img_layout.addWidget(self.img_label)
        img_layout.addStretch()

        layout.addLayout(img_layout)

        # INFO LAPANGAN
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)

        self.lbl_nama = QLabel(lapangan_nama)
        self.lbl_nama.setObjectName("cardTitle")
        
        # MENAMPILKAN TANGGAL DARI DATABASE
        date_layout = QHBoxLayout()

        icon_date = QLabel()
        icon_date.setPixmap(create_colored_icon(os.path.join(BASE_DIR, "assets", "icons", "schedule.svg"), QColor(0,0,0), 18).pixmap(18,18))

        lbl_date = QLabel(tanggal_booking) 
        lbl_date.setObjectName("tggl_book")

        date_layout.addWidget(icon_date)
        date_layout.addWidget(lbl_date)
        date_layout.addStretch()

        time_layout = QHBoxLayout()
        icon_time = QLabel()
        icon_time.setPixmap(create_colored_icon(os.path.join(BASE_DIR, "assets", "icons", "time.svg"), QColor(0,0,0), 18).pixmap(18,18))
        
        self.lbl_time = QLabel(jam_range)
        self.lbl_time.setObjectName("jam")
        
        time_layout.addWidget(icon_time)
        time_layout.addWidget(self.lbl_time)
        time_layout.addStretch()

        loc_layout = QHBoxLayout()
        icon_loc = QLabel()
        icon_loc.setPixmap(create_colored_icon(os.path.join(BASE_DIR, "assets", "icons", "location.svg"), QColor(0,0,0), 18).pixmap(18,18))
        lbl_loc = QLabel("Mataram, Jalan Sriwijaya")
        lbl_loc.setObjectName("lbl")
        loc_layout.addWidget(icon_loc)
        loc_layout.addWidget(lbl_loc)
        loc_layout.addStretch()

        action_layout = QHBoxLayout()
        self.btn_hapus = QPushButton("Hapus")
        self.btn_hapus.setObjectName("btn_hps")
        self.btn_hapus.setIcon(create_colored_icon(os.path.join(BASE_DIR, "assets", "icons", "trash.svg"), QColor("#DC2626"), 16))
        self.btn_hapus.setCursor(Qt.PointingHandCursor)
        self.btn_hapus.setFixedSize(80, 25)

        self.btn_hapus.clicked.connect(lambda: self.delete_clicked.emit(lapangan_nama, tanggal_booking))
        
        action_layout.addWidget(self.btn_hapus)
        action_layout.addStretch()

        info_layout.addWidget(self.lbl_nama)
        info_layout.addLayout(date_layout)
        info_layout.addLayout(time_layout)
        info_layout.addLayout(loc_layout)
        info_layout.addLayout(action_layout)
        info_layout.addStretch()

        layout.addLayout(info_layout)


class HistoryPage(QWidget):
    request_delete = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
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

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(25, 25, 25, 25)
        self.scroll_layout.setSpacing(25)

        self.scroll.setWidget(self.scroll_content)

        # - BOTTOM NAVBAR
        self.bot_nav = BottomNavbar(active_page="history")

        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

        self.top_nav.raise_()
        self.bot_nav.raise_()

    def show_delete_confirmation(self, lapangan_nama, tanggal_booking):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Notifikasi")
        msg_box.setText("Apakah anda ingin menghapus riwayat tersebut?")
        msg_box.setIcon(QMessageBox.Question)
        
        btn_iya = msg_box.addButton("Iya", QMessageBox.YesRole)
        btn_tidak = msg_box.addButton("Tidak", QMessageBox.NoRole)
        
        msg_box.exec()
        
        if msg_box.clickedButton() == btn_iya:
            self.request_delete.emit(lapangan_nama, tanggal_booking)

    def load_history(self, bookings):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if not bookings:
            empty_lbl = QLabel("Belum ada riwayat pemesanan.")
            empty_lbl.setAlignment(Qt.AlignCenter)
            empty_lbl.setStyleSheet("font-size: 16px; color: #71717A;")
            self.scroll_layout.addWidget(empty_lbl)
        else:
            grouped_bookings = {}
            for b in bookings:
                lapangan_nama = b[0]
                tanggal_booking = b[1]
                jam_booking = b[2]
                
                key = (lapangan_nama, tanggal_booking)
                if key not in grouped_bookings:
                    grouped_bookings[key] = []
                grouped_bookings[key].append(jam_booking)

            for (lapangan, tanggal), list_jam in grouped_bookings.items():
                list_jam_sorted = sorted(list_jam)
                jam_gabungan = ", ".join(list_jam_sorted)
                
                card = HistoryCard(lapangan, jam_gabungan, tanggal)
                card.delete_clicked.connect(self.show_delete_confirmation)
                self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch()