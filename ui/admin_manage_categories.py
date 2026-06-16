from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QLineEdit, QAbstractItemView)
from PySide6.QtCore import Qt
from database.db_manager import get_all_categories, add_category, delete_category

class AdminManageCategories(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        self.title = QLabel("Kelola Kategori Olahraga")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #111827;")
        self.layout.addWidget(self.title)

        # Add Category Input
        add_layout = QHBoxLayout()
        add_layout.setSpacing(10)
        
        self.inp_cat = QLineEdit()
        self.inp_cat.setPlaceholderText("Masukkan nama kategori baru...")
        self.inp_cat.setFixedHeight(40)
        self.inp_cat.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #D4D4D8;
                border-radius: 8px;
                padding: 0 15px;
            }
            QLineEdit:focus { border: 1.5px solid #22C55E; }
        """)
        
        self.btn_add = QPushButton("Tambah Kategori")
        self.btn_add.setFixedSize(160, 40)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #22C55E;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #16A34A; }
        """)
        self.btn_add.clicked.connect(self.handle_add)
        
        add_layout.addWidget(self.inp_cat)
        add_layout.addWidget(self.btn_add)
        self.layout.addLayout(add_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nama Kategori", "Aksi"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
                font-weight: bold;
            }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 100)

        self.layout.addWidget(self.table)

    def load_data(self):
        cats = get_all_categories()
        self.table.setRowCount(0)
        
        for row_idx, c in enumerate(cats):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(c[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(c[1]))
            
            btn_delete = QPushButton("Hapus")
            btn_delete.setFixedSize(80, 28)
            btn_delete.setCursor(Qt.PointingHandCursor)
            btn_delete.setStyleSheet("background-color: #EF4444; color: white; border-radius: 4px; font-weight: bold;")
            btn_delete.clicked.connect(lambda checked, id=c[0]: self.handle_delete(id))
            
            # Center the button
            container = QWidget()
            l = QHBoxLayout(container)
            l.setContentsMargins(0, 0, 0, 0)
            l.setAlignment(Qt.AlignCenter)
            l.addWidget(btn_delete)
            
            self.table.setCellWidget(row_idx, 2, container)

    def handle_add(self):
        nama = self.inp_cat.text().strip()
        if not nama: return
        
        if add_category(nama):
            self.inp_cat.clear()
            self.load_data()
        else:
            QMessageBox.warning(self, "Peringatan", "Kategori sudah ada!")

    def handle_delete(self, cat_id):
        reply = QMessageBox.question(self, "Konfirmasi", "Hapus kategori ini?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if delete_category(cat_id):
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus.")
