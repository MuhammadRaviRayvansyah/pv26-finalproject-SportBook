import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont
from database.db_manager import get_admin_stats

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class StatCard(QFrame):
    def __init__(self, title, value, color_hex, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 130)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 20px;
                border: 1px solid #F3F4F6;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(8)

        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #6B7280; font-size: 14px; font-weight: 600; border: none;")
        
        self.lbl_value = QLabel(str(value))
        self.lbl_value.setStyleSheet(f"color: {color_hex}; font-size: 28px; font-weight: 800; border: none;")

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)

class AdminDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # --- HERO HEADER SECTION ---
        self.hero_frame = QFrame()
        self.hero_frame.setFixedHeight(220)
        self.hero_frame.setObjectName("adminHero")
        
        # Gambar Background Hero
        bg_path = os.path.join(BASE_DIR, "assets", "images", "stadium_bg.jpg")
        self.hero_frame.setStyleSheet(f"""
            #adminHero {{
                background-image: url("{bg_path.replace('\\', '/')}");
                background-position: center;
                border-bottom-left-radius: 30px;
                border-bottom-right-radius: 30px;
            }}
        """)
        
        # Overlay untuk teks agar terbaca
        overlay = QFrame(self.hero_frame)
        overlay.setGeometry(0, 0, 2000, 220) # Cukup lebar untuk resize
        overlay.setStyleSheet("background-color: rgba(0, 0, 0, 120); border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;")

        hero_content = QVBoxLayout(self.hero_frame)
        hero_content.setContentsMargins(40, 40, 40, 40)
        hero_content.setSpacing(10)
        
        self.title = QLabel("Admin Control Panel")
        self.title.setStyleSheet("font-size: 32px; font-weight: 800; color: #FFFFFF;")
        
        self.subtitle = QLabel("Pantau performa dan kelola data operasional SportBook Anda.")
        self.subtitle.setStyleSheet("font-size: 16px; color: #E5E7EB; font-weight: 500;")
        
        hero_content.addWidget(self.title)
        hero_content.addWidget(self.subtitle)
        hero_content.addStretch()
        
        self.layout.addWidget(self.hero_frame)

        # --- STATS SECTION ---
        stats_container = QWidget()
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(40, 30, 40, 40)
        
        # Grid untuk kartu statistik
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(25)
        
        self.card_users = StatCard("Total Pengguna", "0", "#3B82F6")
        self.card_bookings = StatCard("Total Pesanan", "0", "#8B5CF6")
        self.card_fields = StatCard("Total Lapangan", "0", "#10B981")
        self.card_revenue = StatCard("Estimasi Pendapatan", "Rp 0", "#F59E0B")
        
        self.stats_grid.addWidget(self.card_users, 0, 0)
        self.stats_grid.addWidget(self.card_bookings, 0, 1)
        self.stats_grid.addWidget(self.card_fields, 0, 2)
        self.stats_grid.addWidget(self.card_revenue, 0, 3)
        
        stats_layout.addLayout(self.stats_grid)
        stats_layout.addStretch()
        
        self.layout.addWidget(stats_container)

    def refresh_data(self):
        stats = get_admin_stats()
        self.card_users.lbl_value.setText(str(stats["users"]))
        self.card_bookings.lbl_value.setText(str(stats["bookings"]))
        self.card_fields.lbl_value.setText(str(stats["fields"]))
        
        revenue_str = f"Rp {stats['revenue']:,}".replace(",", ".")
        self.card_revenue.lbl_value.setText(revenue_str)
