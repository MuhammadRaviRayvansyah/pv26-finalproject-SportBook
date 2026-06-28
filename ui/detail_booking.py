import os
import locale
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QSizePolicy, 
                             QGraphicsDropShadowEffect, QGridLayout, QComboBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath

from ui.navbar import create_colored_icon
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    locale.setlocale(locale.LC_TIME, 'id_ID.utf8')
except:
    pass

class CardImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pixmap = QPixmap()

    def set_image(self, img_path):
        self.pixmap = QPixmap(img_path)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 16, 16)
            painter.setClipPath(path)
            
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.setBrush(QColor("#e5e7eb"))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 16, 16)


class DetailBookingPage(QWidget):
    # DITAMBAHKAN: parameter string untuk mengirim tanggal
    proceed_checkout = Signal(str, list, int, str) 
    go_back = Signal()
    # DITAMBAHKAN: sinyal untuk meminta jam kosong saat tanggal diganti
    request_date_change = Signal(str, str) 

    def __init__(self):
        super().__init__()
        self.lapangan_nama = ""
        self.harga_per_jam = 0
        self.selected_slots = []
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
        self.btn_back.clicked.connect(lambda: self.go_back.emit())
        
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.btn_back)
        left_layout.addStretch()

        self.title_top = QLabel("Booking Lapangan")
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
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(25, 25, 25, 25)
        self.scroll_layout.setSpacing(20)

        # CARD 1: Detail Lapangan
        self.card_detail = QFrame()
        self.card_detail.setObjectName("detailCard")
        shadow1 = QGraphicsDropShadowEffect(self)
        shadow1.setBlurRadius(20)
        shadow1.setXOffset(0)
        shadow1.setYOffset(6)
        shadow1.setColor(QColor(0, 0, 0, 30))
        self.card_detail.setGraphicsEffect(shadow1)

        detail_layout = QVBoxLayout(self.card_detail)
        detail_layout.setContentsMargins(20, 20, 20, 20)
        detail_layout.setSpacing(10)

        self.img_widget = CardImage()
        detail_layout.addWidget(self.img_widget)

        self.lbl_nama = QLabel("Lapangan")
        self.lbl_nama.setObjectName("detailNama")
        self.lbl_nama.setContentsMargins(0, 0, 0, 0)
        detail_layout.addWidget(self.lbl_nama)

        # --- ROW 1: Lokasi ---
        loc_layout = QHBoxLayout()
        loc_layout.setContentsMargins(0, 0, 0, 0)
        loc_layout.setSpacing(8)
        loc_icon = QLabel()
        icon_loc_path = os.path.join(BASE_DIR, "assets", "icons", "location.svg")
        loc_icon.setPixmap(create_colored_icon(icon_loc_path, QColor("#111827"), 18).pixmap(18, 18))
        loc_icon.setFixedSize(18, 18)
        
        lbl_loc_title = QLabel("Lokasi:")
        lbl_loc_title.setObjectName("detailTextBold")
        lbl_loc_title.setFixedWidth(55)
        
        lbl_loc = QLabel("Mataram, Jalan xxxx")
        lbl_loc.setObjectName("detailTextBold")
        
        loc_layout.addWidget(loc_icon)
        loc_layout.addWidget(lbl_loc_title)
        loc_layout.addWidget(lbl_loc)
        loc_layout.addStretch()
        detail_layout.addLayout(loc_layout)

        # --- ROW 2: Buka ---
        buka_layout = QHBoxLayout()
        buka_layout.setContentsMargins(0, 0, 0, 0)
        buka_layout.setSpacing(8)
        buka_icon = QLabel()
        icon_buka_path = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        buka_icon.setPixmap(create_colored_icon(icon_buka_path, QColor("#111827"), 18).pixmap(18, 18))
        buka_icon.setFixedSize(18, 18)
        
        lbl_buka = QLabel("Buka:")
        lbl_buka.setObjectName("detailTextBold")
        lbl_buka.setFixedWidth(55)
        
        buka_layout.addWidget(buka_icon)
        buka_layout.addWidget(lbl_buka)
        buka_layout.addWidget(QLabel("Senin - Minggu", objectName="detailTextBold"))
        buka_layout.addStretch()
        detail_layout.addLayout(buka_layout)

        # --- ROW 3: Jam ---
        jam_layout = QHBoxLayout()
        jam_layout.setContentsMargins(0, 0, 0, 0)
        jam_layout.setSpacing(8)
        jam_icon = QLabel()
        icon_jam_path = os.path.join(BASE_DIR, "assets", "icons", "time.svg")
        jam_icon.setPixmap(create_colored_icon(icon_jam_path, QColor("#111827"), 18).pixmap(18, 18))
        jam_icon.setFixedSize(18, 18)
        
        lbl_jam = QLabel("Jam:")
        lbl_jam.setObjectName("detailTextBold")
        lbl_jam.setFixedWidth(55)
        
        jam_layout.addWidget(jam_icon)
        jam_layout.addWidget(lbl_jam)
        jam_layout.addWidget(QLabel("08.00 - 22.00", objectName="detailTextBold"))
        jam_layout.addStretch()
        detail_layout.addLayout(jam_layout)

        # --- ROW 4: Harga ---
        harga_layout = QHBoxLayout()
        harga_layout.setContentsMargins(0, 0, 0, 0)
        harga_layout.setSpacing(8)
        harga_icon = QLabel()
        icon_harga_path = os.path.join(BASE_DIR, "assets", "icons", "tag.svg")
        harga_icon.setPixmap(create_colored_icon(icon_harga_path, QColor("#111827"), 18).pixmap(18, 18))
        harga_icon.setFixedSize(18, 18)
        
        lbl_harga_title = QLabel("Harga:")
        lbl_harga_title.setObjectName("detailTextBold")
        
        harga_layout.addWidget(harga_icon)
        harga_layout.addWidget(lbl_harga_title)
        harga_layout.addStretch()
        self.lbl_harga = QLabel("0/Jam")
        self.lbl_harga.setObjectName("detailHarga")
        harga_layout.addWidget(self.lbl_harga)
        detail_layout.addLayout(harga_layout)

        self.scroll_layout.addWidget(self.card_detail)

        # =====================================================================
        # DITAMBAHKAN: CARD TANGGAL
        # =====================================================================
        self.card_tanggal = QFrame()
        self.card_tanggal.setObjectName("detailCard")
        shadow_tgl = QGraphicsDropShadowEffect(self)
        shadow_tgl.setBlurRadius(20)
        shadow_tgl.setXOffset(0)
        shadow_tgl.setYOffset(6)
        shadow_tgl.setColor(QColor(0, 0, 0, 30))
        self.card_tanggal.setGraphicsEffect(shadow_tgl)

        tgl_layout = QVBoxLayout(self.card_tanggal)
        tgl_layout.setContentsMargins(20, 15, 20, 15)
        tgl_layout.setSpacing(10)

        lbl_pilih_tgl = QLabel("Pilih Tanggal Booking:")
        lbl_pilih_tgl.setObjectName("detailTextBold")
        tgl_layout.addWidget(lbl_pilih_tgl)

        self.date_combo = QComboBox()
        self.date_combo.setFixedHeight(45)
        self.date_combo.setCursor(Qt.PointingHandCursor)
        self.date_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #D1D5DB;
                border-radius: 10px;
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
                background-color: white;
                color: #111827;
            }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #111827;
                selection-background-color: #22C55E;
                selection-color: white;
                border: 1px solid #D1D5DB;
                outline: none;
            }
        """)
        
        # Isi dropdown 30 hari ke depan
        today = datetime.now()
        for i in range(30):
            date_val = today + timedelta(days=i)
            date_str = date_val.strftime("%d %B %Y")
            self.date_combo.addItem(date_str)
            
        self.date_combo.currentTextChanged.connect(self.on_date_changed)
        tgl_layout.addWidget(self.date_combo)
        
        self.scroll_layout.addWidget(self.card_tanggal)
        # =====================================================================

        # CARD 2: Pilihan Jam
        self.card_jam = QFrame()
        self.card_jam.setObjectName("detailCard")
        shadow2 = QGraphicsDropShadowEffect(self)
        shadow2.setBlurRadius(20)
        shadow2.setXOffset(0)
        shadow2.setYOffset(6)
        shadow2.setColor(QColor(0, 0, 0, 30))
        self.card_jam.setGraphicsEffect(shadow2)

        self.grid_jam = QGridLayout(self.card_jam)
        self.grid_jam.setContentsMargins(20, 20, 20, 20)
        self.grid_jam.setSpacing(15)
        
        self.slot_buttons = {}
        self.scroll_layout.addWidget(self.card_jam)

        # CARD 3: Durasi & Submit
        self.card_submit = QFrame()
        self.card_submit.setObjectName("detailCard")
        shadow3 = QGraphicsDropShadowEffect(self)
        shadow3.setBlurRadius(20)
        shadow3.setXOffset(0)
        shadow3.setYOffset(6)
        shadow3.setColor(QColor(0, 0, 0, 30))
        self.card_submit.setGraphicsEffect(shadow3)

        submit_layout = QVBoxLayout(self.card_submit)
        submit_layout.setContentsMargins(20, 20, 20, 20)
        submit_layout.setSpacing(20)

        durasi_layout = QHBoxLayout()
        durasi_layout.addWidget(QLabel("Durasi", objectName="detailTextBold"))
        durasi_layout.addStretch()
        self.lbl_durasi = QLabel("0 JAM")
        self.lbl_durasi.setObjectName("durasiBadge")
        durasi_layout.addWidget(self.lbl_durasi)
        submit_layout.addLayout(durasi_layout)

        self.btn_next = QPushButton("Berikutnya")
        self.btn_next.setObjectName("btnSubmitGreen")
        self.btn_next.setFixedHeight(50)
        self.btn_next.setCursor(Qt.PointingHandCursor)
        self.btn_next.clicked.connect(self.on_next_clicked)
        submit_layout.addWidget(self.btn_next)

        self.scroll_layout.addWidget(self.card_submit)
        self.scroll_layout.addStretch()

        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        self.top_nav.raise_()

    # DITAMBAHKAN: Fungsi ketika dropdown tanggal diganti
    def on_date_changed(self, new_date):
        self.selected_slots.clear()
        self.lbl_durasi.setText("0 JAM")
        self.request_date_change.emit(self.lapangan_nama, new_date)

    def load_data(self, nama, img_name, harga_int, booked_slots):
        self.lapangan_nama = nama
        self.harga_per_jam = harga_int
        self.selected_slots.clear()
        self.lbl_durasi.setText("0 JAM")

        self.lbl_nama.setText(nama)
        
        harga_str = f"{harga_int:,.0f}".replace(",", ".")
        self.lbl_harga.setText(f"{harga_str}/Jam")

        img_path = os.path.join(BASE_DIR, "assets", "images", img_name)
        self.img_widget.set_image(img_path)

        # DITAMBAHKAN: Reset dropdown ke hari ini tanpa memicu sinyal
        self.date_combo.blockSignals(True)
        self.date_combo.setCurrentIndex(0)
        self.date_combo.blockSignals(False)

        self.build_time_grid(booked_slots)

    # DITAMBAHKAN: Fungsi untuk me-refresh grid saat tanggal diganti
    def refresh_slots(self, booked_slots):
        self.build_time_grid(booked_slots)

    def build_time_grid(self, booked_slots):
        for i in reversed(range(self.grid_jam.count())): 
            self.grid_jam.itemAt(i).widget().setParent(None)
        self.slot_buttons.clear()

        waktu = [
            "08.00 - 09.00", "09.00 - 10.00", "10.00 - 11.00", "11.00 - 12.00",
            "12.00 - 13.00", "13.00 - 14.00", "14.00 - 15.00", "15.00 - 16.00",
            "16.00 - 17.00", "18.00 - 19.00", "20.00 - 21.00", "21.00 - 22.00"
        ]

        row, col = 0, 0
        for jam in waktu:
            btn = QPushButton(jam)
            btn.setObjectName("slotBtn")
            btn.setFixedHeight(35)
            btn.setCursor(Qt.PointingHandCursor)
            
            if jam in booked_slots:
                btn.setProperty("state", "booked")
                btn.setEnabled(False) 
            else:
                btn.setProperty("state", "available")
                btn.clicked.connect(lambda checked, j=jam, b=btn: self.toggle_slot(j, b))

            self.grid_jam.addWidget(btn, row, col)
            self.slot_buttons[jam] = btn

            col += 1
            if col > 3:
                col = 0
                row += 1

    def toggle_slot(self, jam, btn):
        if jam in self.selected_slots:
            self.selected_slots.remove(jam)
            btn.setProperty("state", "available")
        else:
            self.selected_slots.append(jam)
            btn.setProperty("state", "selected")

        btn.style().unpolish(btn)
        btn.style().polish(btn)

        durasi = len(self.selected_slots)
        self.lbl_durasi.setText(f"{durasi} JAM")

    def on_next_clicked(self):
        if not self.selected_slots:
            return 
        
        total_harga = len(self.selected_slots) * self.harga_per_jam
        tanggal_terpilih = self.date_combo.currentText()
        
        # DITAMBAHKAN: Mengirim tanggal terpilih
        self.proceed_checkout.emit(self.lapangan_nama, self.selected_slots, total_harga, tanggal_terpilih)