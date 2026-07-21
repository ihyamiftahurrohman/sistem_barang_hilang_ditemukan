from extensions import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Kategori(db.Model):
    __tablename__ = 'kategori'
    id = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), nullable=False)
    
    # Relationship
    barang = db.relationship('Barang', backref='kategori', lazy=True)

class Barang(db.Model):
    __tablename__ = 'barang'
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(200), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=True)
    warna = db.Column(db.String(50))
    lokasi = db.Column(db.String(200), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    deskripsi = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False) # 'Hilang' atau 'Ditemukan'
    foto = db.Column(db.String(255))
    
    # Relationship
    laporan = db.relationship('Laporan', backref='barang', lazy=True, cascade="all, delete-orphan")

class Laporan(db.Model):
    __tablename__ = 'laporan'
    id = db.Column(db.Integer, primary_key=True)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    nama_pelapor = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    no_hp = db.Column(db.String(20), nullable=False)
    tanggal_lapor = db.Column(db.DateTime, default=datetime.utcnow)
    keterangan = db.Column(db.Text)
