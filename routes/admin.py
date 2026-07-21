from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from models.models import Admin, Kategori, Barang, Laporan

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    """Decorator untuk memastikan admin sudah login."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

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
@login_required
def dashboard():
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

# ==================== KATEGORI ====================
@admin_bp.route('/kategori')
@login_required
def kategori():
    kategoris = Kategori.query.order_by(Kategori.id.desc()).all()
    return render_template('admin/kategori.html', kategoris=kategoris)

@admin_bp.route('/kategori/tambah', methods=['POST'])
@login_required
def kategori_tambah():
    nama = request.form.get('nama_kategori')
    if nama:
        kat = Kategori(nama_kategori=nama)
        db.session.add(kat)
        db.session.commit()
        flash('Kategori berhasil ditambahkan.', 'success')
    else:
        flash('Nama kategori tidak boleh kosong.', 'danger')
    return redirect(url_for('admin.kategori'))

@admin_bp.route('/kategori/hapus/<int:id>')
@login_required
def kategori_hapus(id):
    kat = Kategori.query.get_or_404(id)
    db.session.delete(kat)
    db.session.commit()
    flash('Kategori berhasil dihapus.', 'success')
    return redirect(url_for('admin.kategori'))

# ==================== DATA BARANG ====================
@admin_bp.route('/barang')
@login_required
def barang():
    barangs = Barang.query.order_by(Barang.id.desc()).all()
    return render_template('admin/barang.html', barangs=barangs)

@admin_bp.route('/barang/hapus/<int:id>')
@login_required
def barang_hapus(id):
    brg = Barang.query.get_or_404(id)
    db.session.delete(brg)
    db.session.commit()
    flash('Data barang berhasil dihapus.', 'success')
    return redirect(url_for('admin.barang'))

# ==================== LAPORAN MASUK ====================
@admin_bp.route('/laporan')
@login_required
def laporan():
    laporans = Laporan.query.order_by(Laporan.id.desc()).all()
    return render_template('admin/laporan.html', laporans=laporans)

@admin_bp.route('/laporan/hapus/<int:id>')
@login_required
def laporan_hapus(id):
    lap = Laporan.query.get_or_404(id)
    db.session.delete(lap)
    db.session.commit()
    flash('Laporan berhasil dihapus.', 'success')
    return redirect(url_for('admin.laporan'))

