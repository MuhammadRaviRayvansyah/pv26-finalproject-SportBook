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
    
    # Tabel Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Tabel Bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_nama TEXT NOT NULL,
            lapangan_nama TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            jam_booking TEXT NOT NULL
        )
    ''')

    # Tabel Lapangan (Baru)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lapangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            gambar TEXT NOT NULL,
            harga TEXT NOT NULL,
            deskripsi TEXT,
            kategori TEXT
        )
    ''')

    # Tabel Kategori (Baru)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kategori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT UNIQUE NOT NULL
        )
    ''')
    
    # --- MIGRASI DATA AWAL ---
    
    # 1. Tambah Admin Default jika belum ada
    cursor.execute("SELECT * FROM users WHERE email='admin@sportbook.com'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (nama, email, password, role) VALUES (?, ?, ?, ?)",
                       ("Admin SportBook", "admin@sportbook.com", "admin123", "admin"))

    # 2. Tambah Kategori Default
    default_categories = ["Futsal", "Basket", "Badminton"]
    for cat in default_categories:
        cursor.execute("INSERT OR IGNORE INTO kategori (nama) VALUES (?)", (cat,))

    # 3. Tambah Lapangan Default jika tabel kosong
    cursor.execute("SELECT COUNT(*) FROM lapangan")
    if cursor.fetchone()[0] == 0:
        default_fields = [
            ("Lapangan 1", "lapangan_1.jpg", "200.000", "Lapangan futsal dengan rumput sintetis berkualitas.", "Futsal"),
            ("Lapangan 2", "lapangan_2.jpg", "200.000", "Lapangan basket indoor dengan lantai kayu standar internasional.", "Basket"),
            ("Lapangan 3", "lapangan_3.jpg", "200.000", "Lapangan badminton dengan karpet standar PBSI.", "Badminton")
        ]
        cursor.executemany("INSERT INTO lapangan (nama, gambar, harga, deskripsi, kategori) VALUES (?, ?, ?, ?, ?)", default_fields)

    conn.commit()
    conn.close()

# --- FUNGSI CRUD LAPANGAN ---

def get_all_fields():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama, gambar, harga, deskripsi, kategori FROM lapangan ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_field(nama, gambar, harga, deskripsi, kategori):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO lapangan (nama, gambar, harga, deskripsi, kategori) VALUES (?, ?, ?, ?, ?)",
                       (nama, gambar, harga, deskripsi, kategori))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error add field: {e}")
        return False
    finally:
        conn.close()

def update_field(field_id, nama, gambar, harga, deskripsi, kategori):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE lapangan SET nama=?, gambar=?, harga=?, deskripsi=?, kategori=? WHERE id=?",
                       (nama, gambar, harga, deskripsi, field_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error update field: {e}")
        return False
    finally:
        conn.close()

def delete_field(field_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM lapangan WHERE id=?", (field_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error delete field: {e}")
        return False
    finally:
        conn.close()

# --- FUNGSI CRUD KATEGORI ---

def get_all_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama FROM kategori ORDER BY nama ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_category(nama):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO kategori (nama) VALUES (?)", (nama,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_category(cat_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM kategori WHERE id=?", (cat_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error delete category: {e}")
        return False
    finally:
        conn.close()

# --- FUNGSI STATISTIK ADMIN ---

def get_all_bookings_admin():
    """Mengambil seluruh daftar booking untuk Admin."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_nama, lapangan_nama, tanggal, jam_booking FROM bookings ORDER BY id DESC")
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
    
    # Estimasi pendapatan (Total booking * harga rata-rata 200rb sebagai dummy logic sederhana)
    # Jika ingin akurat, harus simpan harga di tabel bookings
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

def validate_login(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nama, role FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

# --- FUNGSI BARU UNTUK BOOKING ---

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
    """Mengambil semua riwayat booking milik user tertentu."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Kita ambil nama lapangan dan jamnya
    cursor.execute("SELECT lapangan_nama, tanggal, jam_booking FROM bookings WHERE user_nama=? ORDER BY id DESC", (user_nama,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user_booking(user_nama, lapangan_nama, tanggal):
    """Menghapus riwayat booking berdasarkan user dan lapangan."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE user_nama=? AND lapangan_nama=? AND tanggal=?", (user_nama, lapangan_nama, tanggal))
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