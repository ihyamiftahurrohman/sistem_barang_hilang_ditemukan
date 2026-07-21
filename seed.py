from app import create_app
from extensions import db, bcrypt
from models.models import Admin, Kategori

app = create_app()

with app.app_context():
    # Buat semua tabel
    db.create_all()

    # Cek apakah admin sudah ada
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        new_admin = Admin(username='admin', password_hash=hashed_password)
        db.session.add(new_admin)
        print("Admin user 'admin' created with password 'admin123'")

    # Cek kategori default
    if Kategori.query.count() == 0:
        kategoris = ['Elektronik', 'Dokumen', 'Pakaian', 'Aksesoris', 'Lainnya']
        for nama in kategoris:
            kat = Kategori(nama_kategori=nama)
            db.session.add(kat)
        print("Default categories created.")

    db.session.commit()
    print("Database seeding completed.")
