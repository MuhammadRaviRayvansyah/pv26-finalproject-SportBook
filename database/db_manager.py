import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "sportbook.db")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabel Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # 2. Tabel Bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_nama TEXT NOT NULL,
            lapangan_nama TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            jam_booking TEXT NOT NULL,
            "status" TEXT DEFAULT 'active'
        )
    ''')

    # 3. Tabel Lapangan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lapangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            gambar TEXT NOT NULL,
            harga TEXT NOT NULL
        )
    ''')
    
    
    # Tambah Admin Default
    cursor.execute("SELECT * FROM users WHERE email='admin@sportbook.com'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (nama, email, password, role) VALUES (?, ?, ?, ?)",
                       ("Admin SportBook", "admin@sportbook.com", "admin123", "admin"))

    # Tambah Lapangan Default
    cursor.execute("SELECT COUNT(*) FROM lapangan")
    # if True:
    if cursor.fetchone()[0] == 0:
        default_fields = [
            ("Lapangan 1", "lapangan_1.jpg", "200.000"),
            ("Lapangan 2", "lapangan_2.jpg", "200.000"),
            ("Lapangan 3", "lapangan_3.jpg", "200.000"),
            ("Lapangan 4", "lapangan_3.jpg", "200.000")
        ]
        cursor.executemany("INSERT INTO lapangan (nama, gambar, harga) VALUES (?, ?, ?)", default_fields)

    conn.commit()
    conn.close()

# FUNGSI AMBIL DATA LAPANGAN (DIPAKAI OLEH USER)
def get_all_fields():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama, gambar, harga, deskripsi FROM lapangan ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# FUNGSI STATISTIK ADMIN
def get_all_bookings_admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Mengambil semua data tanpa filter status, sehingga data yang 'deleted' pun tetap tampil
    cursor.execute('SELECT user_nama, lapangan_nama, tanggal, jam_booking FROM bookings ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_admin_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM lapangan")
    total_fields = cursor.fetchone()[0]

    total_revenue = total_bookings * 200000
    
    conn.close()
    return {
        "users": total_users,
        "bookings": total_bookings,
        "fields": total_fields,
        "revenue": total_revenue
    }

def register_user(nama, email, password, role='user'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (nama, email, password, role) VALUES (?, ?, ?, ?)", 
                       (nama, email, password, role))
        conn.commit()
        return True, "Akun berhasil dibuat! Silakan masuk."
    except sqlite3.IntegrityError:
        return False, "Email tersebut sudah terdaftar!"
    finally:
        conn.close()

def validate_login(nama, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nama, role FROM users WHERE  nama=? AND password=?", (nama, password))
    user = cursor.fetchone()
    conn.close()
    return user

# FUNGSI BARU UNTUK BOOKING
def get_booked_slots(lapangan_nama, tanggal):
    """Mengambil daftar jam yang sudah dibooking untuk lapangan tertentu."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT jam_booking FROM bookings WHERE lapangan_nama=? AND tanggal=?", (lapangan_nama, tanggal))
    rows = cursor.fetchall()
    conn.close()
    
    # Format return: list of strings (cth: ["08.00 - 09.00", "12.00 - 13.00"])
    return [row[0] for row in rows]

def save_booking(user_nama, lapangan_nama, tanggal, list_jam):
    """Menyimpan banyak jam booking sekaligus ke dalam database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        for jam in list_jam:
            cursor.execute("INSERT INTO bookings (user_nama, lapangan_nama, tanggal, jam_booking) VALUES (?, ?, ?, ?)",
                           (user_nama, lapangan_nama, tanggal, jam))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving booking: {e}")
        return False
    finally:
        conn.close()

def get_user_bookings(user_nama):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Menambahkan WHERE "status" = 'active'
    cursor.execute('SELECT lapangan_nama, tanggal, jam_booking FROM bookings WHERE user_nama=? AND "status" = "active" ORDER BY id DESC', (user_nama,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user_booking(user_nama, lapangan_nama, tanggal):
    """Menyembunyikan riwayat dari User, tapi Admin tetap bisa melihatnya."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Mengubah status menjadi 'deleted' alih-alih menghapus baris
    cursor.execute('UPDATE bookings SET "status" = "deleted" WHERE user_nama=? AND lapangan_nama=? AND tanggal=?', 
                   (user_nama, lapangan_nama, tanggal))
    conn.commit()
    conn.close()

def update_user_profile(old_nama, new_nama, new_password):
    """Memperbarui nama dan/atau password pengguna di database secara permanen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # PERBAIKAN: Mengganti 'username' menjadi 'nama' menyesuaikan kolom di database Anda
    if new_password:
        cursor.execute("UPDATE users SET nama=?, password=? WHERE nama=?", (new_nama, new_password, old_nama))
    else:
        cursor.execute("UPDATE users SET nama=? WHERE nama=?", (new_nama, old_nama))
        
    # Update juga nama di tabel bookings agar riwayat transaksi lama tidak hilang
    if old_nama != new_nama:
        cursor.execute("UPDATE bookings SET user_nama=? WHERE user_nama=?", (new_nama, old_nama))
        
    conn.commit()
    conn.close()
    return True