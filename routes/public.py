from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from extensions import db
from models.models import Kategori, Barang, Laporan, Kontak

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    total_hilang = Barang.query.filter_by(status='Hilang').count()
    total_ditemukan = Barang.query.filter_by(status='Ditemukan').count()
    return render_template('public/index.html', total_hilang=total_hilang, total_ditemukan=total_ditemukan)

@public_bp.route('/tentang')
def tentang():
    return render_template('public/tentang.html')

@public_bp.route('/kontak')
def kontak():
    kontak_info = Kontak.query.first()
    return render_template('public/kontak.html', kontak=kontak_info)

@public_bp.route('/barang-hilang')
def barang_hilang():
    barangs = Barang.query.filter_by(status='Hilang').order_by(Barang.tanggal.desc()).all()
    return render_template('public/barang_hilang.html', barangs=barangs)

@public_bp.route('/barang-ditemukan')
def barang_ditemukan():
    barangs = Barang.query.filter_by(status='Ditemukan').order_by(Barang.tanggal.desc()).all()
    return render_template('public/barang_ditemukan.html', barangs=barangs)

@public_bp.route('/barang/<int:id>')
def detail_barang(id):
    barang = Barang.query.get_or_404(id)
    return render_template('public/detail_barang.html', barang=barang)

@public_bp.route('/lapor-hilang', methods=['GET', 'POST'])
def lapor_hilang():
    kategoris = Kategori.query.all()
    if request.method == 'POST':
        nama_barang = request.form.get('nama_barang')
        kategori_id = request.form.get('kategori_id')
        warna = request.form.get('warna')
        lokasi = request.form.get('lokasi')
        tanggal_str = request.form.get('tanggal')
        deskripsi = request.form.get('deskripsi')
        
        nama_pelapor = request.form.get('nama_pelapor')
        email = request.form.get('email')
        no_hp = request.form.get('no_hp')
        
        # Handle file upload
        foto = request.files.get('foto')
        filename = None
        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            foto_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            foto.save(foto_path)
            
        try:
            tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
            
            # Buat record Barang baru
            barang = Barang(
                nama_barang=nama_barang,
                kategori_id=kategori_id,
                warna=warna,
                lokasi=lokasi,
                tanggal=tanggal,
                deskripsi=deskripsi,
                status='Hilang',
                foto=filename
            )
            db.session.add(barang)
            db.session.flush() # Agar mendapatkan barang.id
            
            # Buat record Laporan
            laporan = Laporan(
                barang_id=barang.id,
                nama_pelapor=nama_pelapor,
                email=email,
                no_hp=no_hp,
                keterangan="Melaporkan kehilangan barang."
            )
            db.session.add(laporan)
            db.session.commit()
            
            flash('Laporan barang hilang berhasil disubmit!', 'success')
            return redirect(url_for('public.barang_hilang'))
            
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan data.', 'danger')
            print(f"Error: {e}")
            
    return render_template('public/form_lapor_hilang.html', kategoris=kategoris)

@public_bp.route('/lapor-ditemukan', methods=['GET', 'POST'])
def lapor_ditemukan():
    kategoris = Kategori.query.all()
    if request.method == 'POST':
        nama_barang = request.form.get('nama_barang')
        kategori_id = request.form.get('kategori_id')
        warna = request.form.get('warna')
        lokasi = request.form.get('lokasi')
        tanggal_str = request.form.get('tanggal')
        deskripsi = request.form.get('deskripsi')
        
        nama_pelapor = request.form.get('nama_pelapor')
        email = request.form.get('email')
        no_hp = request.form.get('no_hp')
        
        # Handle file upload
        foto = request.files.get('foto')
        filename = None
        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            foto_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            foto.save(foto_path)
            
        try:
            tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
            
            # Buat record Barang baru dengan status Ditemukan
            barang = Barang(
                nama_barang=nama_barang,
                kategori_id=kategori_id,
                warna=warna,
                lokasi=lokasi,
                tanggal=tanggal,
                deskripsi=deskripsi,
                status='Ditemukan',
                foto=filename
            )
            db.session.add(barang)
            db.session.flush() # Agar mendapatkan barang.id
            
            # Buat record Laporan
            laporan = Laporan(
                barang_id=barang.id,
                nama_pelapor=nama_pelapor,
                email=email,
                no_hp=no_hp,
                keterangan="Melaporkan penemuan barang."
            )
            db.session.add(laporan)
            db.session.commit()
            
            flash('Laporan barang ditemukan berhasil disubmit!', 'success')
            return redirect(url_for('public.barang_ditemukan'))
            
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan data.', 'danger')
            print(f"Error: {e}")
            
    return render_template('public/form_lapor_ditemukan.html', kategoris=kategoris)
