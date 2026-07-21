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
        from models.models import Admin, Kategori
        db.create_all()
        
        # Pastikan akun admin default tersedia
        if not Admin.query.first():
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            new_admin = Admin(username='admin', password_hash=hashed_password)
            db.session.add(new_admin)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
