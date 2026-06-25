import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QFrame, 
                               QGraphicsDropShadowEffect, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

class AdminPengaturan(QWidget):
    # Signal ini akan memancarkan (emit) nama baru dan kata sandi baru ke main.py
    save_clicked = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Layout utama halaman dikunci marginnya ke 0 untuk menempel ke tepi layar
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- 1. HEADER SECTION (Mengikuti style admin_dashboard) ---
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
        
        lbl_title = QLabel("Pengaturan Akun Admin")
        lbl_title.setStyleSheet("font-size: 28px; font-weight: 800; color: #111827; border: none; background: transparent;")
        
        lbl_subtitle = QLabel("Perbarui informasi kredensial nama dan kata sandi Anda.")
        lbl_subtitle.setStyleSheet("font-size: 14px; color: #6B7280; font-weight: 500; border: none; background: transparent;")
        
        hero_content.addWidget(lbl_title)
        hero_content.addWidget(lbl_subtitle)
        
        main_layout.addWidget(self.hero_frame)

        # --- 2. CONTAINER KONTEN (Background disamakan dengan dashboard) ---
        content_container = QWidget()
        content_container.setStyleSheet("background-color: #F9FAFB;")
        
        # Margin 40px diletakkan di container ini agar jarak kartu rapi
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(40, 30, 40, 40)
        
        # --- 3. KARTU FORMULIR (TIDAK ADA YANG DIUBAH SAMA SEKALI) ---
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
            QLabel {
                border: none;
                font-size: 14px;
                color: #374151;
                font-weight: 600;
            }
            QLineEdit {
                padding: 12px 15px;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                background-color: #F9FAFB;
                font-size: 14px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #10B981;
                background-color: #FFFFFF;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        lbl_nama = QLabel("Nama Admin:")
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Masukkan nama admin yang baru")
        
        lbl_sandi = QLabel("Kata Sandi Baru:")
        self.input_sandi = QLineEdit()
        self.input_sandi.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_sandi.setPlaceholderText("Masukkan kata sandi baru (kosongkan jika tidak ingin mengubah)")
        
        self.btn_simpan = QPushButton("Simpan Perubahan")
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.setFixedSize(200, 45)
        self.btn_simpan.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.btn_simpan.clicked.connect(self.handle_save)
        
        card_layout.addWidget(lbl_nama)
        card_layout.addWidget(self.input_nama)
        card_layout.addWidget(lbl_sandi)
        card_layout.addWidget(self.input_sandi)
        
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 15, 0, 0)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_simpan)
        
        card_layout.addLayout(btn_layout)
        
        # --- MEMASUKKAN KARTU KE DALAM CONTENT CONTAINER ---
        content_layout.addWidget(card)
        content_layout.addStretch()
        
        # Memasukkan content container ke layout utama
        main_layout.addWidget(content_container)
        
    def set_current_nama(self, nama_sekarang):
        self.input_nama.setText(nama_sekarang)
        self.input_sandi.clear()
        
    def handle_save(self):
        nama_baru = self.input_nama.text().strip()
        sandi_baru = self.input_sandi.text().strip()
        
        if not nama_baru:
            QMessageBox.warning(self, "Peringatan", "Kolom nama tidak boleh kosong!")
            return
            
        self.save_clicked.emit(nama_baru, sandi_baru)