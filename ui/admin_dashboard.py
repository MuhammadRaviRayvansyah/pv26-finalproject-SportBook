import os
import csv
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QGraphicsDropShadowEffect,
                             QScrollArea, QPushButton, QFileDialog, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

from database.db_manager import get_admin_stats

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class StatCard(QFrame):
    def __init__(self, title, color_hex, parent=None):
        super().__init__(parent)
        # Diperkecil tingginya dan menggunakan SizePolicy agar lebar merenggang otomatis (Horizontal)
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #6B7280; font-size: 12px; font-weight: 600; border: none;")
        
        # Angka 0 hanya sementara, akan langsung diisi dari database saat aplikasi berjalan
        self.lbl_value = QLabel("0")
        self.lbl_value.setStyleSheet(f"color: {color_hex}; font-size: 24px; font-weight: 800; border: none;")

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)


class ChartCard(QFrame):
    def __init__(self, title, color_hex, parent=None):
        super().__init__(parent)
        self.setFixedHeight(260)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        
        lbl_title = QLabel(f"Grafik {title}")
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151; border: none; padding-left: 10px;")
        layout.addWidget(lbl_title)

        # Inisialisasi Chart (Bar Chart Sederhana)
        self.series = QBarSeries()
        self.bar_set = QBarSet(title)
        self.bar_set.setColor(QColor(color_hex))
        self.bar_set.append(0) 
        self.series.append(self.bar_set)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(["Total"])
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("border: none;")
        layout.addWidget(self.chart_view)

    def update_chart(self, value):
        # Memperbarui isi grafik sesuai data dari database
        self.bar_set.replace(0, value)
        max_y = value + (value * 0.2) if value > 0 else 10
        self.axis_y.setRange(0, max_y)


class AdminDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        # Langsung menarik data dari database saat halaman dibuka (Tidak statis)
        self.refresh_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Membuat area scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F9FAFB; }")
        
        self.container = QWidget()
        self.container.setStyleSheet("background-color: #F9FAFB;")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 30)
        self.layout.setSpacing(20)

        # 1. --- HERO HEADER SECTION (Teks Saja, Tanpa Gambar) ---
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
        
        self.title = QLabel("Admin Control Panel")
        self.title.setStyleSheet("font-size: 28px; font-weight: 800; color: #111827; border: none;")
        
        self.subtitle = QLabel("Pantau performa dan kelola data operasional SportBook Anda.")
        self.subtitle.setStyleSheet("font-size: 14px; color: #6B7280; font-weight: 500; border: none;")
        
        hero_content.addWidget(self.title)
        hero_content.addWidget(self.subtitle)
        
        self.layout.addWidget(self.hero_frame)

        # 2. --- STATS SECTION (Kecil, Horizontal 1 Baris) ---
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container) # Menggunakan Horizontal Box
        stats_layout.setContentsMargins(40, 10, 40, 10)
        stats_layout.setSpacing(15)
        
        self.card_users = StatCard("Total Pengguna", "#3B82F6")
        self.card_bookings = StatCard("Total Pesanan", "#8B5CF6")
        self.card_fields = StatCard("Total Lapangan", "#10B981")
        self.card_revenue = StatCard("Estimasi Pendapatan", "#F59E0B")
        
        stats_layout.addWidget(self.card_users)
        stats_layout.addWidget(self.card_bookings)
        stats_layout.addWidget(self.card_fields)
        stats_layout.addWidget(self.card_revenue)
        
        self.layout.addWidget(stats_container)

        # 3. --- CHARTS SECTION (Grafik dalam Card) ---
        charts_container = QWidget()
        charts_layout = QGridLayout(charts_container)
        charts_layout.setContentsMargins(40, 10, 40, 10)
        charts_layout.setSpacing(15)

        self.chart_users = ChartCard("Pengguna", "#3B82F6")
        self.chart_bookings = ChartCard("Pesanan", "#8B5CF6")
        self.chart_fields = ChartCard("Lapangan", "#10B981")
        self.chart_revenue = ChartCard("Pendapatan", "#F59E0B")

        # Disusun menjadi grid 2x2
        charts_layout.addWidget(self.chart_users, 0, 0)
        charts_layout.addWidget(self.chart_bookings, 0, 1)
        charts_layout.addWidget(self.chart_fields, 1, 0)
        charts_layout.addWidget(self.chart_revenue, 1, 1)

        self.layout.addWidget(charts_container)

        # 4. --- EXPORT CSV BUTTON SECTION ---
        export_container = QWidget()
        export_layout = QHBoxLayout(export_container)
        export_layout.setContentsMargins(40, 20, 40, 20)
        export_layout.setAlignment(Qt.AlignRight) # Tombol berada di kanan

        self.btn_export = QPushButton(" Export Data ke CSV")
        self.btn_export.setFixedSize(180, 45)
        self.btn_export.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.clicked.connect(self.export_csv)

        export_layout.addWidget(self.btn_export)
        self.layout.addWidget(export_container)

        self.layout.addStretch()
        
        # Memasukkan container utama ke dalam area scroll
        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

    def refresh_data(self):
        # Mengambil data dari database
        stats = get_admin_stats()
        
        # Update teks di 4 Stat Cards
        self.card_users.lbl_value.setText(str(stats["users"]))
        self.card_bookings.lbl_value.setText(str(stats["bookings"]))
        self.card_fields.lbl_value.setText(str(stats["fields"]))
        revenue_str = f"Rp {stats['revenue']:,}".replace(",", ".")
        self.card_revenue.lbl_value.setText(revenue_str)

        # Update grafik di 4 Chart Cards
        self.chart_users.update_chart(stats["users"])
        self.chart_bookings.update_chart(stats["bookings"])
        self.chart_fields.update_chart(stats["fields"])
        self.chart_revenue.update_chart(stats["revenue"])

    def export_csv(self):
        # Membuka dialog untuk menyimpan file CSV
        path, _ = QFileDialog.getSaveFileName(self, "Simpan Laporan CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                # Tarik data terbaru sebelum export
                stats = get_admin_stats()
                
                with open(path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';') # Menggunakan pemisah ';' agar rapi di Excel
                    writer.writerow(["Kategori", "Total"])
                    writer.writerow(["Total Pengguna", stats["users"]])
                    writer.writerow(["Total Pesanan", stats["bookings"]])
                    writer.writerow(["Total Lapangan", stats["fields"]])
                    writer.writerow(["Estimasi Pendapatan", stats["revenue"]])
                
                QMessageBox.information(self, "Sukses", f"Data berhasil diexport!\nTersimpan di:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal mengekspor data ke CSV.\n\nDetail:\n{e}")