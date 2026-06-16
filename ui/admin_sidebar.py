import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QFrame, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QColor, QPainter, QIcon

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_colored_icon(icon_path, color, size=24):
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

class AdminSidebar(QFrame):
    nav_changed = Signal(str) # "dashboard", "fields", "bookings", "categories", "logout"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setObjectName("adminSidebar")
        self.setStyleSheet("""
            #adminSidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
            }
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                color: #4B5563;
                background: transparent;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
                color: #111827;
            }
            QPushButton#activeNav {
                background-color: #F0FDF4;
                color: #16A34A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 30, 15, 20)
        layout.setSpacing(8)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png")
        pixmap_logo = QPixmap(logo_path)
        if not pixmap_logo.isNull():
            logo_label.setPixmap(pixmap_logo.scaled(160, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setContentsMargins(0, 0, 0, 30)
        layout.addWidget(logo_label)

        # Menu Buttons
        self.btn_dashboard = self._create_nav_btn("Dashboard", "home.svg", "dashboard")
        self.btn_fields = self._create_nav_btn("Kelola Lapangan", "schedule.svg", "fields")
        self.btn_bookings = self._create_nav_btn("Daftar Pesanan", "history.svg", "bookings")
        self.btn_categories = self._create_nav_btn("Kelola Kategori", "tag.svg", "categories")
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_fields)
        layout.addWidget(self.btn_bookings)
        layout.addWidget(self.btn_categories)
        
        layout.addStretch()

        # Logout Button
        self.btn_logout = self._create_nav_btn("Keluar", "logout.svg", "logout", is_logout=True)
        layout.addWidget(self.btn_logout)

        self.buttons = [self.btn_dashboard, self.btn_fields, self.btn_bookings, self.btn_categories]
        self.set_active("dashboard")

    def _create_nav_btn(self, text, icon_name, nav_target, is_logout=False):
        btn = QPushButton(f"  {text}")
        icon_path = os.path.join(BASE_DIR, "assets", "icons", icon_name)
        color = QColor("#EF4444") if is_logout else QColor("#4B5563")
        btn.setIcon(create_colored_icon(icon_path, color, 20))
        btn.setIconSize(QSize(20, 20))
        btn.setCursor(Qt.PointingHandCursor)
        
        if is_logout:
            btn.setStyleSheet("color: #EF4444; font-weight: bold;")
            btn.clicked.connect(lambda: self.nav_changed.emit("logout"))
        else:
            btn.clicked.connect(lambda: self._handle_click(btn, nav_target))
        
        return btn

    def _handle_click(self, btn, target):
        self.set_active(target)
        self.nav_changed.emit(target)

    def set_active(self, target):
        for b in self.buttons:
            b.setObjectName("")
        
        active_btn = None
        if target == "dashboard": active_btn = self.btn_dashboard
        elif target == "fields": active_btn = self.btn_fields
        elif target == "bookings": active_btn = self.btn_bookings
        elif target == "categories": active_btn = self.btn_categories
        
        if active_btn:
            active_btn.setObjectName("activeNav")
        
        # Refresh stylesheet to apply objectName changes
        self.setStyleSheet(self.styleSheet())
