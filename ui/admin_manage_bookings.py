import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QAbstractItemView, QFrame)
from PySide6.QtCore import Qt
from database.db_manager import get_all_bookings_admin

class AdminManageBookings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        header_container = QVBoxLayout()
        self.title = QLabel("Daftar Pesanan Lapangan")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #111827;")
        self.subtitle = QLabel("Lihat siapa saja yang telah melakukan booking lapangan.")
        self.subtitle.setStyleSheet("font-size: 14px; color: #6B7280;")
        header_container.addWidget(self.title)
        header_container.addWidget(self.subtitle)
        self.layout.addLayout(header_container)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nama User", "Lapangan", "Tanggal", "Jam"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                gridline-color: #F3F4F6;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
                font-weight: bold;
                color: #374151;
            }
            QTableWidget::item {
                padding: 12px;
                color: #4B5563;
            }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table)

    def load_data(self):
        bookings = get_all_bookings_admin()
        self.table.setRowCount(0)
        
        for row_idx, b in enumerate(bookings):
            # b: (user_nama, lapangan_nama, tanggal, jam_booking)
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(b[0]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(b[1]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(b[2]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(b[3]))
