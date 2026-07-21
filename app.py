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
        import models.models
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
