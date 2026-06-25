import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QAbstractItemView, QFrame, QLineEdit, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from database.db_manager import get_all_bookings_admin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AdminManageBookings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_bookings = [] 
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # --- 1. HERO HEADER SECTION ---
        self.hero_frame = QFrame()
        self.hero_frame.setFixedHeight(120)
        self.hero_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
            }
        """)

        hero_content = QVBoxLayout(self.hero_frame)
        hero_content.setContentsMargins(40, 25, 40, 25)

        self.title = QLabel("Daftar Pesanan Lapangan")
        self.title.setStyleSheet("font-size: 28px; font-weight: 800; color: #111827; border: none; background: transparent;")

        self.subtitle = QLabel("Lihat siapa saja yang telah melakukan booking lapangan.")
        self.subtitle.setStyleSheet("font-size: 14px; color: #6B7280; font-weight: 500; border: none; background: transparent;")

        hero_content.addWidget(self.title)
        hero_content.addWidget(self.subtitle)

        self.layout.addWidget(self.hero_frame)

        # --- 2. CONTENT CONTAINER ---
        content_container = QWidget()
        content_container.setStyleSheet("background-color: #F9FAFB;")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(40, 30, 40, 40)
        content_layout.setSpacing(15) 

        # --- 3. SEARCH & FILTER SECTION ---
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        # Input Pencarian Teks (Dengan Icon SVG)
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Cari nama pengguna...")
        
        # Menambahkan icon SVG ke dalam kolom pencarian (di sisi kiri/Leading)
        search_icon_path = os.path.join(BASE_DIR, "assets", "icons", "search.svg")
        self.inp_search.addAction(QIcon(search_icon_path), QLineEdit.LeadingPosition)
        
        self.inp_search.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #10B981;
            }
        """)
        self.inp_search.textChanged.connect(self.apply_filter)

        # Dropdown Filter Tanggal (Dengan perbaikan QAbstractItemView)
        self.combo_filter = QComboBox()
        self.combo_filter.addItem("Semua Tanggal")
        self.combo_filter.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                color: #374151;
                min-width: 160px;
            }
            QComboBox:focus {
                border: 2px solid #10B981;
            }
            /* Perbaikan agar daftar dropdown dapat terlihat jelas */
            QComboBox QAbstractItemView {
                background-color: white;
                color: #374151;
                selection-background-color: #F3F4F6;
                selection-color: #111827;
                border: 1px solid #D1D5DB;
                outline: none;
            }
        """)
        self.combo_filter.currentTextChanged.connect(self.apply_filter)

        filter_layout.addWidget(self.inp_search, stretch=3)
        filter_layout.addWidget(self.combo_filter, stretch=1)
        content_layout.addLayout(filter_layout)

        # --- 4. PENGATURAN TABEL ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nama User", "Lapangan", "Tanggal", "Jam"])
        
        self.table.setSelectionMode(QAbstractItemView.NoSelection) 
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                gridline-color: #F3F4F6;
                font-size: 15px;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 15px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                font-weight: bold;
                font-size: 16px;
                color: #374151;
            }
            QTableWidget::item {
                padding: 10px;
                color: #4B5563;
                border-bottom: 1px solid #F3F4F6;
            }
            QTableWidget::item:hover {
                background-color: transparent;
                color: #4B5563;
            }
        """)

        header = self.table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        content_layout.addWidget(self.table)
        self.layout.addWidget(content_container)

    def load_data(self):
        self.all_bookings = get_all_bookings_admin()
        
        # Mengambil daftar tanggal yang unik dari database
        unique_dates = set()
        for b in self.all_bookings:
            unique_dates.add(b[2]) # Indeks 2 adalah kolom tanggal
            
        # Memperbarui isi dropdown filter dengan tanggal yang tersedia
        self.combo_filter.blockSignals(True) 
        self.combo_filter.clear()
        self.combo_filter.addItem("Semua Tanggal")
        self.combo_filter.addItems(sorted(list(unique_dates)))
        self.combo_filter.blockSignals(False)
        
        self.apply_filter()

    def apply_filter(self):
        search_query = self.inp_search.text().strip().lower()
        selected_date = self.combo_filter.currentText()

        self.table.setRowCount(0)
        row_idx = 0

        for b in self.all_bookings:
            user_nama, lapangan_nama, tanggal, jam_booking = b
            
            # Evaluasi kecocokan filter dropdown tanggal
            match_date = (selected_date == "Semua Tanggal" or selected_date == tanggal)
            
            # Evaluasi kecocokan pencarian nama pengguna
            match_name = (search_query in user_nama.lower())

            # Masukkan data ke tabel hanya jika memenuhi kedua filter
            if match_date and match_name:
                self.table.insertRow(row_idx)
                for col_idx in range(4):
                    item = QTableWidgetItem(b[col_idx])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)
                row_idx += 1