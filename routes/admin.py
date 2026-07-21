from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from models.models import Admin, Kategori, Barang, Laporan

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and bcrypt.check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('admin.login'))
        
    total_barang = Barang.query.count()
    total_hilang = Barang.query.filter_by(status='Hilang').count()
    total_ditemukan = Barang.query.filter_by(status='Ditemukan').count()
    total_laporan = Laporan.query.count()
    total_kategori = Kategori.query.count()
    
    return render_template('admin/dashboard.html', 
                           total_barang=total_barang,
                           total_hilang=total_hilang,
                           total_ditemukan=total_ditemukan,
                           total_laporan=total_laporan,
                           total_kategori=total_kategori)
