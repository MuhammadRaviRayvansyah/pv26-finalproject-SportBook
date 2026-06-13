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
    
    # Tabel Bookings (Baru)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_nama TEXT NOT NULL,
            lapangan_nama TEXT NOT NULL,
            jam_booking TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

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

def get_booked_slots(lapangan_nama):
    """Mengambil daftar jam yang sudah dibooking untuk lapangan tertentu."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT jam_booking FROM bookings WHERE lapangan_nama=?", (lapangan_nama,))
    rows = cursor.fetchall()
    conn.close()
    
    # Format return: list of strings (cth: ["08.00 - 09.00", "12.00 - 13.00"])
    return [row[0] for row in rows]

def save_booking(user_nama, lapangan_nama, list_jam):
    """Menyimpan banyak jam booking sekaligus ke dalam database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        for jam in list_jam:
            cursor.execute("INSERT INTO bookings (user_nama, lapangan_nama, jam_booking) VALUES (?, ?, ?)",
                           (user_nama, lapangan_nama, jam))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving booking: {e}")
        return False
    finally:
        conn.close()