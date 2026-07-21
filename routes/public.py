from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return render_template('public/index.html')

@public_bp.route('/tentang')
def tentang():
    return render_template('public/tentang.html')

@public_bp.route('/kontak')
def kontak():
    return render_template('public/kontak.html')

@public_bp.route('/barang-hilang')
def barang_hilang():
    return render_template('public/barang_hilang.html')

@public_bp.route('/barang-ditemukan')
def barang_ditemukan():
    return render_template('public/barang_ditemukan.html')

@public_bp.route('/barang/<int:id>')
def detail_barang(id):
    return render_template('public/detail_barang.html', id=id)

@public_bp.route('/lapor-hilang', methods=['GET', 'POST'])
def lapor_hilang():
    return render_template('public/form_lapor_hilang.html')

@public_bp.route('/lapor-ditemukan', methods=['GET', 'POST'])
def lapor_ditemukan():
    return render_template('public/form_lapor_ditemukan.html')
