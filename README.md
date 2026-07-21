# Sistem Informasi Pendataan Barang Hilang dan Ditemukan Berbasis Web untuk di Lingkungan Kampus

Aplikasi ini adalah Sistem Informasi berbasis web yang dibangun menggunakan **Flask (Python)** untuk mempermudah civitas akademika di lingkungan kampus dalam melaporkan dan mencari barang yang hilang atau ditemukan.

## 🚀 Fitur Utama

- **Halaman Publik**:
  - Melihat daftar barang yang hilang.
  - Melihat daftar barang yang ditemukan.
  - Melaporkan barang yang hilang.
  - Melaporkan barang yang ditemukan.
  - Halaman informasi kontak.

- **Halaman Admin**:
  - Dashboard statistik barang dan laporan.
  - Manajemen Kategori Barang.
  - Manajemen Data Barang (Tambah, Edit, Hapus).
  - Manajemen Laporan dari pengguna.
  - Manajemen Informasi Kontak.
  - Sistem Login yang aman dengan *hashing* password.

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python 3, Flask
- **Database**: SQLite (via Flask-SQLAlchemy)
- **Keamanan**: Flask-Bcrypt (untuk hashing password)
- **Frontend**: HTML, CSS, Template Jinja2

## 📦 Prasyarat

Pastikan Anda telah menginstal **Python 3.x** di sistem Anda.

## ⚙️ Cara Instalasi dan Menjalankan Aplikasi

1. **Buka terminal/command prompt**, lalu navigasikan ke folder project:
   ```bash
   cd "Sistem Informasi Pendataan Barang Hilang dan Ditemukan Berbasis Web untuk  di Lingkungan Kampus"
   ```

2. **Buat Virtual Environment** (direkomendasikan):
   ```bash
   python -m venv venv
   ```

3. **Aktifkan Virtual Environment**:
   - Di **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - Di **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Instal Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Seed Data** (Opsional, untuk mengisi data awal kategori jika diperlukan):
   ```bash
   python seed.py
   ```
   *(Aplikasi secara otomatis membuat akun admin default pada saat pertama kali dijalankan, serta struktur database).*

6. **Jalankan Aplikasi**:
   ```bash
   python app.py
   ```

7. **Akses Aplikasi**:
   - Buka browser dan kunjungi: `http://127.0.0.1:5000`
   - **Halaman Admin**: `http://127.0.0.1:5000/admin`
     - **Username Default**: `admin`
     - **Password Default**: `admin123`

## 📂 Struktur Direktori Utama

- `app.py`: File utama aplikasi yang mengatur inisialisasi Flask, database, dan routing (Blueprint).
- `config.py`: File konfigurasi aplikasi (termasuk *secret key*, database URI, konfigurasi upload maksimal 5MB).
- `models/`: Berisi definisi skema database untuk tabel Admin, Kategori, Barang, Laporan, dan Kontak.
- `routes/`: Berisi alur pengontrol (*controllers*) untuk halaman Publik dan Admin.
- `templates/`: Berisi file HTML/Jinja2 untuk tampilan antarmuka aplikasi.
- `static/`: Berisi file statis seperti CSS, gambar, dan folder `uploads` tempat menyimpan foto barang.
- `database/`: Folder tempat file database SQLite (`app.db`) disimpan.

## 📝 Catatan Penting
- Folder `static/uploads` akan secara otomatis dibuat oleh aplikasi jika belum ada untuk menyimpan gambar foto barang (dibatasi 5 MB).
- Data kontak *default* dan admin *default* akan otomatis dibuat ke database saat aplikasi dijalankan pertama kali.
