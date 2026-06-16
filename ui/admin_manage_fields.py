import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from database.db_manager import get_all_fields, delete_field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AdminManageFields(QWidget):
    request_add = Signal()
    request_edit = Signal(dict) # field data

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        
        title_container = QVBoxLayout()
        self.title = QLabel("Kelola Data Lapangan")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #111827;")
        self.subtitle = QLabel("Tambah, ubah, atau hapus data lapangan olahraga.")
        self.subtitle.setStyleSheet("font-size: 14px; color: #6B7280;")
        title_container.addWidget(self.title)
        title_container.addWidget(self.subtitle)
        
        self.btn_add = QPushButton("+ Tambah Lapangan")
        self.btn_add.setFixedSize(180, 40)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #22C55E;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
        """)
        self.btn_add.clicked.connect(lambda: self.request_add.emit())

        header_layout.addLayout(title_container)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add)
        
        self.layout.addLayout(header_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Foto", "Nama Lapangan", "Kategori", "Harga", "Aksi"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60) # Tinggi baris agar thumbnail terlihat
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                gridline-color: #F3F4F6;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
                font-weight: bold;
                color: #374151;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #4B5563;
                border-bottom: 1px solid #F3F4F6;
            }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 80)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 180)

        self.layout.addWidget(self.table)

    def load_data(self):
        fields = get_all_fields()
        self.table.setRowCount(0)
        
        for row_idx, f in enumerate(fields):
            self.table.insertRow(row_idx)
            
            # f: (id, nama, gambar, harga, deskripsi, kategori)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(f[0])))
            
            # Thumbnail Foto
            img_label = QLabel()
            img_path = os.path.join(BASE_DIR, "assets", "images", f[2])
            pixmap = QPixmap(img_path)
            if not pixmap.isNull():
                img_label.setPixmap(pixmap.scaled(60, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row_idx, 1, img_label)

            self.table.setItem(row_idx, 2, QTableWidgetItem(f[1]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f[5]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"Rp {f[3]}"))
            
            # Action Buttons
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(5, 2, 5, 2)
            btn_layout.setSpacing(10)
            
            btn_edit = QPushButton("Edit")
            btn_edit.setFixedSize(70, 28)
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setStyleSheet("background-color: #3B82F6; color: white; border-radius: 4px; font-weight: bold;")
            field_data = {"id": f[0], "nama": f[1], "gambar": f[2], "harga": f[3], "deskripsi": f[4], "kategori": f[5]}
            btn_edit.clicked.connect(lambda checked, d=field_data: self.request_edit.emit(d))
            
            btn_delete = QPushButton("Hapus")
            btn_delete.setFixedSize(70, 28)
            btn_delete.setCursor(Qt.PointingHandCursor)
            btn_delete.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; font-weight: bold;")
            btn_delete.clicked.connect(lambda checked, id=f[0]: self.handle_delete(id))
            
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)
            
            self.table.setCellWidget(row_idx, 4, btn_container)

    def handle_delete(self, field_id):
        reply = QMessageBox.question(self, "Konfirmasi", "Apakah Anda yakin ingin menghapus lapangan ini?", 
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if delete_field(field_id):
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus data.")
