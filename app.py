from flask import Flask
from config import Config
from extensions import db, bcrypt
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi ekstensi
    db.init_app(app)
    bcrypt.init_app(app)

    # Buat direktori upload jika belum ada
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Registrasi blueprint
    from routes.public import public_bp
    from routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Buat tabel database (jika belum ada)
    with app.app_context():
        from models.models import Admin, Kategori, Kontak
        db.create_all()
        
        # Pastikan akun admin default tersedia
        if not Admin.query.first():
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            new_admin = Admin(username='admin', password_hash=hashed_password)
            db.session.add(new_admin)
            
        # Pastikan data kontak default tersedia
        if not Kontak.query.first():
            default_kontak = Kontak(
                deskripsi="Jika Anda memiliki pertanyaan, kendala, atau membutuhkan bantuan terkait barang yang hilang/ditemukan, jangan ragu untuk menghubungi kami melalui kontak di bawah ini.",
                alamat="Gedung Pusat Administrasi<br>Lantai 1, Ruang Kemahasiswaan",
                email="kemahasiswaan@kampus.ac.id",
                telepon="+62 812 3456 7890"
            )
            db.session.add(default_kontak)
            
        db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
