import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QComboBox, 
                             QFileDialog, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal
from database.db_manager import get_all_categories, add_field, update_field

class AdminFieldForm(QWidget):
    go_back = Signal()
    save_success = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.field_id = None # None means Add, otherwise Edit
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        self.btn_back = QPushButton("< Kembali")
        self.btn_back.setFixedSize(100, 30)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setStyleSheet("border: none; color: #6B7280; font-weight: bold; text-align: left;")
        self.btn_back.clicked.connect(lambda: self.go_back.emit())
        self.layout.addWidget(self.btn_back)

        self.title = QLabel("Form Lapangan")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #111827;")
        self.layout.addWidget(self.title)

        # Form Card
        self.card = QFrame()
        self.card.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #E5E7EB;")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        # Nama
        card_layout.addWidget(QLabel("Nama Lapangan"))
        self.inp_nama = QLineEdit()
        self.inp_nama.setPlaceholderText("Contoh: Lapangan Futsal A")
        card_layout.addWidget(self.inp_nama)

        # Kategori
        card_layout.addWidget(QLabel("Kategori"))
        self.cmb_kategori = QComboBox()
        card_layout.addWidget(self.cmb_kategori)

        # Harga
        card_layout.addWidget(QLabel("Harga per Jam (Format: 200.000)"))
        self.inp_harga = QLineEdit()
        self.inp_harga.setPlaceholderText("200.000")
        card_layout.addWidget(self.inp_harga)

        # Deskripsi
        card_layout.addWidget(QLabel("Deskripsi"))
        self.inp_desc = QTextEdit()
        self.inp_desc.setPlaceholderText("Jelaskan detail lapangan...")
        self.inp_desc.setFixedHeight(100)
        card_layout.addWidget(self.inp_desc)

        # Gambar
        card_layout.addWidget(QLabel("Nama File Gambar (di assets/images/)"))
        self.inp_gambar = QLineEdit()
        self.inp_gambar.setPlaceholderText("lapangan_1.jpg")
        card_layout.addWidget(self.inp_gambar)

        self.layout.addWidget(self.card)

        # Submit
        self.btn_save = QPushButton("Simpan Data")
        self.btn_save.setFixedSize(200, 45)
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #22C55E;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
        """)
        self.btn_save.clicked.connect(self.handle_save)
        self.layout.addWidget(self.btn_save, 0, Qt.AlignCenter)
        
        self.layout.addStretch()

    def load_form(self, data=None):
        # Refresh Categories
        self.cmb_kategori.clear()
        categories = get_all_categories()
        for cat in categories:
            self.cmb_kategori.addItem(cat[1])

        if data:
            self.field_id = data["id"]
            self.title.setText("Edit Data Lapangan")
            self.inp_nama.setText(data["nama"])
            self.inp_harga.setText(data["harga"])
            self.inp_desc.setPlainText(data["deskripsi"])
            self.inp_gambar.setText(data["gambar"])
            
            idx = self.cmb_kategori.findText(data["kategori"])
            if idx >= 0: self.cmb_kategori.setCurrentIndex(idx)
        else:
            self.field_id = None
            self.title.setText("Tambah Lapangan Baru")
            self.inp_nama.clear()
            self.inp_harga.clear()
            self.inp_desc.clear()
            self.inp_gambar.clear()

    def handle_save(self):
        nama = self.inp_nama.text().strip()
        harga = self.inp_harga.text().strip()
        desc = self.inp_desc.toPlainText().strip()
        gambar = self.inp_gambar.text().strip()
        kategori = self.cmb_kategori.currentText()

        if not nama or not harga or not gambar:
            QMessageBox.warning(self, "Peringatan", "Nama, Harga, dan Gambar wajib diisi!")
            return

        if self.field_id:
            res = update_field(self.field_id, nama, gambar, harga, desc, kategori)
        else:
            res = add_field(nama, gambar, harga, desc, kategori)

        if res:
            QMessageBox.information(self, "Sukses", "Data lapangan berhasil disimpan!")
            self.save_success.emit()
        else:
            QMessageBox.critical(self, "Error", "Gagal menyimpan data ke database.")
