# Mengimpor modul os untuk berinteraksi dengan sistem operasi, khususnya untuk manajemen path (jalur file)
import os

# Mengimpor komponen-komponen antarmuka pengguna (UI) dari PySide6
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QSizePolicy, 
                             QGraphicsDropShadowEffect, QToolButton)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath, QIcon

# Menentukan direktori dasar (BASE_DIR) dari proyek dengan mengambil dua tingkat direktori ke atas dari file ini
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fungsi utilitas untuk membuat ikon yang warnanya dapat disesuaikan (berguna untuk ikon SVG)
def create_colored_icon(icon_path, color, size=28):

    # Memuat gambar dari jalur file yang diberikan
    pixmap = QPixmap(icon_path)
    
    # Memeriksa apakah gambar berhasil dimuat
    if not pixmap.isNull():
        # Mengubah ukuran gambar sesuai parameter 'size' dengan menjaga rasio aspek dan memperhalus tepiannya
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # Membuat kanvas (pixmap) baru dengan ukuran yang sama untuk diwarnai
        colored_pixmap = QPixmap(pixmap.size())
        # Mengisi kanvas dengan warna transparan
        colored_pixmap.fill(Qt.transparent)
        
        # Menginisialisasi QPainter untuk menggambar di atas kanvas baru
        painter = QPainter(colored_pixmap)
        # Mengaktifkan antialiasing agar gambar tidak bergerigi
        painter.setRenderHint(QPainter.Antialiasing)
        # Menggambar gambar asli ke kanvas
        painter.drawPixmap(0, 0, pixmap)
        # Mengatur mode komposisi agar warna yang diisi hanya menimpa bagian gambar yang tidak transparan
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        # Mengisi seluruh kanvas dengan warna yang diinginkan (parameter 'color')
        painter.fillRect(colored_pixmap.rect(), color)
        # Mengakhiri proses menggambar
        painter.end()
        
        # Mengembalikan gambar yang sudah diwarnai dalam bentuk QIcon
        return QIcon(colored_pixmap)
    # Mengembalikan QIcon kosong jika gambar gagal dimuat
    return QIcon()

# Kelas untuk membuat komponen banner pahlawan (Hero Section) di bagian atas beranda
class HeroFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Mengatur nama objek untuk keperluan styling (QSS)
        self.setObjectName("heroSection")
        # Mengatur tinggi tetap sebesar 320 piksel
        self.setFixedHeight(320)
        # Mendefinisikan jalur file gambar latar belakang (background stadium)
        self.bg_path = os.path.join(BASE_DIR, "assets", "images", "stadium_bg.jpg")
        self.pixmap = QPixmap(self.bg_path)
        
        # Memberikan efek bayangan (drop shadow) pada frame Hero
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20) # Tingkat keburaman bayangan
        shadow.setXOffset(0)     # Pergeseran bayangan sumbu X
        shadow.setYOffset(6)     # Pergeseran bayangan sumbu Y
        shadow.setColor(QColor(0, 0, 0, 45)) # Warna bayangan (Hitam transparan)
        self.setGraphicsEffect(shadow)

    # Memodifikasi cara frame digambar untuk memberikan efek sudut melengkung dan background gambar
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Jika gambar latar belakang berhasil dimuat
        if not self.pixmap.isNull():
            # Menskalakan gambar agar memenuhi ukuran frame
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # Membuat jalur (path) dengan sudut melengkung sebesar 24 piksel
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 24, 24)
            # Memotong (clip) area gambar agar mengikuti bentuk sudut melengkung
            painter.setClipPath(path)
            
            # Menghitung posisi X dan Y agar gambar berada tepat di tengah (center crop)
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            # Menggambar gambar latar belakang
            painter.drawPixmap(x, y, scaled)
        else:
            # Jika gambar tidak ditemukan, gunakan warna abu-abu sebagai fallback dengan sudut melengkung
            painter.setBrush(QColor("#e5e7eb"))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 24, 24)

# Kelas widget khusus untuk merender gambar lapangan dengan sudut melengkung
class CardImage(QWidget):
    def __init__(self, img_path, parent=None):
        super().__init__(parent)
        # Mengatur tinggi tetap gambar menjadi 240 piksel
        self.setFixedHeight(240)
        # Mengatur ukuran agar lebarnya melar mengikuti kontainer, tapi tingginya tetap
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Memuat gambar dari jalur yang diberikan
        self.pixmap = QPixmap(img_path)

    # Memodifikasi cara gambar dirender agar memiliki sudut melengkung
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.pixmap.isNull():
            # Menskalakan gambar
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # Membuat mask dengan sudut melengkung sebesar 14 piksel
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 14, 14)
            painter.setClipPath(path)
            
            # Menempatkan gambar di tengah (center crop)
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            # Fallback warna abu-abu jika gambar tidak ditemukan
            painter.setBrush(QColor("#e5e7eb"))
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)

# Kelas untuk komponen Kartu Lapangan (menampilkan info detail lapangan di beranda)
class FieldCard(QFrame):
    # Sinyal kustom yang dikirim saat tombol booking pada kartu ini diklik
    request_book = Signal(str, str, int)

    def __init__(self, img_name, title, price_str, parent=None):
        super().__init__(parent)
        self.setObjectName("fieldCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Membersihkan string harga (menghapus titik) dan mengonversinya ke integer
        self.harga_int = int(price_str.replace(".", ""))
        
        # Menambahkan efek bayangan pada kartu
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 45))
        self.setGraphicsEffect(shadow)

        # Tata letak utama kartu (vertikal)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(15) 

        # Bagian 1: Widget Gambar Melengkung
        img_path = os.path.join(BASE_DIR, "assets", "images", img_name)
        self.img_widget = CardImage(img_path)
        main_layout.addWidget(self.img_widget)

        # Bagian 2: Area Informasi (Judul, Lokasi, Buka, Jam)
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(8) 
        
        # Judul Lapangan
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("cardTitle")
        self.title_lbl.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(self.title_lbl)
        
        # Baris Informasi Lokasi
        loc_layout = QHBoxLayout()
        loc_layout.setContentsMargins(0, 0, 0, 0)
        loc_layout.setSpacing(8)
        loc_icon = QLabel()
        icon_loc_path = os.path.join(BASE_DIR, "assets", "icons", "location.svg")
        # Memberi warna ikon lokasi
        loc_icon.setPixmap(create_colored_icon(icon_loc_path, QColor("#111827"), 18).pixmap(20, 20))
        loc_icon.setFixedSize(20, 20)
        loc_icon.setAlignment(Qt.AlignCenter)
        
        lbl_loc_title = QLabel("Lokasi:")
        lbl_loc_title.setStyleSheet("color: #000000; font-weight: bold;")
        lbl_loc_title.setFixedWidth(55)
        lbl_loc = QLabel("Mataram, Jalan xxxx")
        lbl_loc.setStyleSheet("color: #000000; font-weight: bold;")
        
        loc_layout.addWidget(loc_icon)
        loc_layout.addWidget(lbl_loc_title)
        loc_layout.addWidget(lbl_loc)
        loc_layout.addStretch()
        info_layout.addLayout(loc_layout)

        # Baris Informasi Hari Buka
        buka_layout = QHBoxLayout()
        buka_layout.setContentsMargins(0, 0, 0, 0)
        buka_layout.setSpacing(8)
        buka_icon = QLabel()
        icon_buka_path = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        buka_icon.setPixmap(create_colored_icon(icon_buka_path, QColor("#111827"), 18).pixmap(20, 20))
        buka_icon.setFixedSize(20, 20)
        buka_icon.setAlignment(Qt.AlignCenter)
        
        lbl_buka = QLabel("Buka:")
        lbl_buka.setStyleSheet("color: #000000; font-weight: bold;")
        lbl_buka.setFixedWidth(55)
        lbl_buka_val = QLabel("Senin - Minggu")
        lbl_buka_val.setStyleSheet("color: #000000; font-weight: bold;")
        
        buka_layout.addWidget(buka_icon)
        buka_layout.addWidget(lbl_buka)
        buka_layout.addWidget(lbl_buka_val)
        buka_layout.addStretch()
        info_layout.addLayout(buka_layout)

        # Baris Informasi Jam Operasional
        jam_layout = QHBoxLayout()
        jam_layout.setContentsMargins(0, 0, 0, 0)
        jam_layout.setSpacing(8)
        jam_icon = QLabel()
        icon_jam_path = os.path.join(BASE_DIR, "assets", "icons", "time.svg")
        jam_icon.setPixmap(create_colored_icon(icon_jam_path, QColor("#111827"), 18).pixmap(20, 20))
        jam_icon.setFixedSize(20, 20)
        jam_icon.setAlignment(Qt.AlignCenter)
        
        lbl_jam = QLabel("Jam:")
        lbl_jam.setStyleSheet("color: #000000; font-weight: bold;")
        lbl_jam.setFixedWidth(55)
        lbl_jam_val = QLabel("08.00 - 22.00")
        lbl_jam_val.setStyleSheet("color: #000000; font-weight: bold;")
        
        jam_layout.addWidget(jam_icon)
        jam_layout.addWidget(lbl_jam)
        jam_layout.addWidget(lbl_jam_val)
        jam_layout.addStretch()
        info_layout.addLayout(jam_layout)

        # Menambahkan area informasi ke layout utama kartu
        main_layout.addLayout(info_layout)

        # Bagian 3: Area Harga dan Tombol Booking
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        
        # Kelompok Harga (Label "Harga" dan Nilai Harga)
        price_group = QVBoxLayout()
        price_group.setContentsMargins(0, 0, 0, 0)
        price_group.setSpacing(0)
        self.price_tag = QLabel("Harga")
        self.price_tag.setObjectName("cardDesc")
        self.price_tag.setContentsMargins(0, 0, 0, 0)
        self.price_tag.setStyleSheet("color: #000000; font-weight: bold;")
        
        self.price_val = QLabel(f"{price_str}/Jam")
        self.price_val.setObjectName("cardPrice")
        self.price_val.setContentsMargins(0, 0, 0, 0)
        
        price_group.addWidget(self.price_tag)
        price_group.addWidget(self.price_val)
        
        # Tombol Booking
        self.btn_book = QPushButton("Booking Lapangan")
        self.btn_book.setObjectName("btnCardAction")
        self.btn_book.setFixedSize(150, 42)
        self.btn_book.setCursor(Qt.PointingHandCursor)
        
        # Menghubungkan klik tombol dengan sinyal 'request_book'
        self.btn_book.clicked.connect(lambda: self.request_book.emit(title, img_name, self.harga_int))
        
        # Memasukkan elemen harga dan tombol ke area bawah
        bottom_layout.addLayout(price_group)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_book)

        # Menambahkan area bawah ke layout utama kartu
        main_layout.addLayout(bottom_layout)

# Kelas Induk untuk Halaman Utama (Beranda)
class HomePage(QWidget):
    # Sinyal kustom untuk meneruskan permintaan booking dari dalam FieldCard ke Main Window
    request_book = Signal(str, str, int)

    def __init__(self):
        super().__init__()
        # Memanggil metode inisialisasi antarmuka
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("homePage")
        # Tata letak utama halaman beranda
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- BAGIAN 1: TOP NAVBAR (Navigasi Atas) ---
        self.top_nav = QFrame()
        self.top_nav.setObjectName("topNav")
        self.top_nav.setFixedHeight(65)
        
        # Memberikan bayangan pada navbar atas
        shadow_top = QGraphicsDropShadowEffect(self)
        shadow_top.setBlurRadius(15)
        shadow_top.setXOffset(0)
        shadow_top.setYOffset(4)
        shadow_top.setColor(QColor(0, 0, 0, 20))
        self.top_nav.setGraphicsEffect(shadow_top)

        top_layout = QHBoxLayout(self.top_nav)
        top_layout.setContentsMargins(25, 0, 25, 0)

        # Logo Aplikasi di kiri
        self.logo = QLabel()
        pix_logo = QPixmap(os.path.join(BASE_DIR, "assets", "logos", "sportbook_logo.png"))
        if not pix_logo.isNull():
            self.logo.setPixmap(pix_logo.scaled(130, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Profil Pengguna di kanan
        user_layout = QHBoxLayout()
        user_layout.setSpacing(12)
        self.user_name = QLabel("Ravi")
        self.user_name.setObjectName("userName")
        
        # Ikon profil pengguna
        self.icon_user = QLabel()
        user_icon_path = os.path.join(BASE_DIR, "assets", "icons", "user.svg")
        user_pixmap = QPixmap(user_icon_path)
        if not user_pixmap.isNull():
            self.icon_user.setPixmap(user_pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_user.setFixedSize(22, 22)
        self.icon_user.setCursor(Qt.PointingHandCursor)
        
        user_layout.addWidget(self.user_name)
        user_layout.addWidget(self.icon_user)

        top_layout.addWidget(self.logo)
        top_layout.addStretch() # Spacer untuk mendorong profil ke kanan
        top_layout.addLayout(user_layout)

        # --- BAGIAN 2: SCROLL AREA (Area Konten Utama) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True) # Agar konten menyesuaikan lebar window
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setObjectName("contentScroll")
        # Menyembunyikan scrollbar
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Widget sebagai penampung seluruh konten di dalam Scroll Area
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        # --- KONTEN DALAM (HERO SECTION + LIST LAPANGAN) ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)

        # Menginisialisasi komponen HeroFrame
        self.hero = HeroFrame()
        hero_layout = QVBoxLayout(self.hero)
        hero_layout.setContentsMargins(35, 30, 35, 30)
        hero_layout.setSpacing(12)
        
        # Teks sambutan di dalam Hero
        self.h_title = QLabel("Hallo, <b style='color:#22C55E;'>Pengguna!</b>")
        self.h_title.setObjectName("heroTitle")

        self.h_sub1 = QLabel("Booking futsal hari ini?")
        self.h_sub1.setObjectName("heroSub")
        self.h_sub1.setContentsMargins(0, 5, 0, 0)

        self.h_sub2 = QLabel("Terdapat pilihan lapangan dan jam booking")
        self.h_sub2.setObjectName("heroSub")
        self.h_sub2.setContentsMargins(0, 0, 0, 10)
        
        # Tombol informasi lokasi di Hero
        self.loc_badge = QPushButton(" Lokasi: Mataram, Jalan xxxx")
        self.loc_badge.setObjectName("locBadge")
        self.loc_badge.setFixedSize(220, 42)
        self.loc_badge.setCursor(Qt.PointingHandCursor)
        self.loc_badge.setContentsMargins(0, 5, 0, 5)
        
        icon_loc_path = os.path.join(BASE_DIR, "assets", "icons", "location.svg")
        self.loc_badge.setIcon(create_colored_icon(icon_loc_path, QColor(255, 255, 255), 18))
        self.loc_badge.setIconSize(QSize(18, 18))
        
        # Tombol Booking utama di Hero
        self.btn_hero = QPushButton("Booking Sekarang")
        self.btn_hero.setObjectName("btnHero")
        self.btn_hero.setFixedSize(220, 42)
        self.btn_hero.setCursor(Qt.PointingHandCursor)
        self.btn_hero.setContentsMargins(0, 10, 0, 0)

        # Memasukkan elemen ke tata letak Hero
        hero_layout.addWidget(self.h_title)
        hero_layout.addWidget(self.h_sub1)
        hero_layout.addWidget(self.h_sub2)
        hero_layout.addStretch() # Mendorong tombol ke area bawah Hero
        hero_layout.addWidget(self.loc_badge)
        hero_layout.addWidget(self.btn_hero)
        
        content_layout.addWidget(self.hero)
        
        # Judul untuk seksi list lapangan
        self.list_title = QLabel("List Lapangan")
        self.list_title.setObjectName("sectionTitle")
        self.list_title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.list_title)

        # Kontainer kosong untuk menampung kartu lapangan yang digenerate secara dinamis
        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_container)
        
        # PERBAIKAN: Ubah margin bawah dari 0 menjadi 25 agar shadow kartu terakhir memiliki ruang
        self.fields_layout.setContentsMargins(0, 0, 0, 25) 
        
        self.fields_layout.setSpacing(25)
        content_layout.addWidget(self.fields_container)

        self.scroll_layout.addWidget(content_widget)
        self.scroll.setWidget(self.scroll_content)

        # --- BAGIAN 3: BOTTOM NAVBAR (Navigasi Bawah) ---
        self.bot_nav = QFrame()
        self.bot_nav.setFixedHeight(75)
        # Mengizinkan pewarnaan background lewat stylesheet
        self.bot_nav.setAttribute(Qt.WA_StyledBackground, True)
        self.bot_nav.setStyleSheet("background-color: white;")
        
        # Bayangan navbar bawah
        shadow_bot = QGraphicsDropShadowEffect(self)
        shadow_bot.setBlurRadius(20)
        shadow_bot.setXOffset(0)
        shadow_bot.setYOffset(-4) # Nilai negatif agar bayangan mengarah ke atas
        shadow_bot.setColor(QColor(0, 0, 0, 20))
        self.bot_nav.setGraphicsEffect(shadow_bot)

        bot_layout = QHBoxLayout(self.bot_nav)
        bot_layout.setContentsMargins(0, 5, 0, 5) 
        bot_layout.setSpacing(0) 

        # Jalur ikon untuk menu bawah
        icon_home = os.path.join(BASE_DIR, "assets", "icons", "home.svg")
        icon_schedule = os.path.join(BASE_DIR, "assets", "icons", "schedule.svg")
        icon_history = os.path.join(BASE_DIR, "assets", "icons", "history.svg")
        icon_gear = os.path.join(BASE_DIR, "assets", "icons", "gear.svg")

        # Tombol Menu Beranda (Diatur sebagai status aktif/hijau)
        self.btn_home = QToolButton()
        self.btn_home.setIcon(create_colored_icon(icon_home, QColor(34, 197, 94), 28)) 
        self.btn_home.setText("Beranda")
        self.btn_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_home.setCursor(Qt.PointingHandCursor)
        self.btn_home.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.btn_home.setStyleSheet("color: #22C55E; border: none; font-size: 13px; font-weight: bold;")

        # Tombol Menu Booking
        self.btn_booking = QToolButton()
        self.btn_booking.setIcon(create_colored_icon(icon_schedule, QColor(113, 113, 122), 28)) 
        self.btn_booking.setText("Booking")
        self.btn_booking.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_booking.setCursor(Qt.PointingHandCursor)
        self.btn_booking.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_booking.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        # Tombol Menu Riwayat
        self.btn_hist = QToolButton()
        self.btn_hist.setIcon(create_colored_icon(icon_history, QColor(113, 113, 122), 28)) 
        self.btn_hist.setText("Riwayat")
        self.btn_hist.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_hist.setCursor(Qt.PointingHandCursor)
        self.btn_hist.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_hist.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        # Tombol Menu Pengaturan
        self.btn_settings = QToolButton()
        self.btn_settings.setIcon(create_colored_icon(icon_gear, QColor(113, 113, 122), 28)) 
        self.btn_settings.setText("Pengaturan")
        self.btn_settings.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_settings.setStyleSheet("color: #71717A; border: none; font-size: 13px; font-weight: bold;")

        # Menambahkan seluruh tombol ke tata letak navbar bawah
        bot_layout.addWidget(self.btn_home)
        bot_layout.addWidget(self.btn_booking)
        bot_layout.addWidget(self.btn_hist)
        bot_layout.addWidget(self.btn_settings)

        # Merakit semua komponen ke tata letak utama halaman
        self.main_layout.addWidget(self.top_nav)
        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.bot_nav)

        # Memastikan navbar tetap berada di layer paling atas
        self.top_nav.raise_()
        self.bot_nav.raise_()

        # Menghubungkan tombol hero agar memiliki aksi yang sama dengan tombol menu booking
        self.btn_hero.clicked.connect(self.btn_booking.click)

    # Fungsi untuk memuat data lapangan dari database dan merendernya ke antarmuka
    def load_dynamic_fields(self, fields):
        # Membersihkan widget/layout lama sebelum merender data baru
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Iterasi seluruh data lapangan yang dikirim
        for f in fields:
            # Menginisialisasi objek Kartu Lapangan (indeks 2: gambar, indeks 1: nama, indeks 3: harga)
            card = FieldCard(f[2], f[1], f[3])
            # Mengaitkan sinyal klik pada kartu agar diteruskan ke Main Window
            card.request_book.connect(self.request_book.emit)
            # Menambahkan kartu ke dalam kontainer
            self.fields_layout.addWidget(card)