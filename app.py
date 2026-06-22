#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PUSAT SEMBAKO - Sistem Informasi Penjualan dan Manajemen Inventory
Version: 1.0.0
Author: Development Team

This is a complete Flask web application for managing a sembako (grocery) store
with admin, cashier, and customer features.
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from functools import wraps
from io import BytesIO
import secrets
import string

from flask import (
    Flask, render_template, request, jsonify, redirect, url_for, 
    session, send_file, send_from_directory, flash
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, and_, or_
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import pytz

# =============================================================================
# FLASK APP INITIALIZATION
# =============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pusat_sembako.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'writable/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Load config from config.json
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except:
    config_data = {}

db = SQLAlchemy(app)

# Create necessary directories
os.makedirs('app/templates/admin', exist_ok=True)
os.makedirs('app/templates/cashier', exist_ok=True)
os.makedirs('app/templates/customer', exist_ok=True)
os.makedirs('app/static/css', exist_ok=True)
os.makedirs('app/static/js', exist_ok=True)
os.makedirs('public/assets/products', exist_ok=True)
os.makedirs('public/assets/variants', exist_ok=True)
os.makedirs('public/assets/banners', exist_ok=True)
os.makedirs('public/assets/logos', exist_ok=True)
os.makedirs('writable/uploads', exist_ok=True)
os.makedirs('writable/logs', exist_ok=True)
os.makedirs('writable/invoices', exist_ok=True)

# =============================================================================
# DATABASE MODELS
# =============================================================================

class Role(db.Model):
    """Role model for user roles"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # admin, cashier, customer
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    """User model for admin and cashier"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='cashier')  # admin, cashier
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Member(db.Model):
    """Member model for customers with loyalty program"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    member_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text)
    points = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Member {self.nama}>'


class Category(db.Model):
    """Product category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi = db.Column(db.Text)
    icon = db.Column(db.String(255))  # path to icon/image
    urutan = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    products = db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.nama}>'


class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    deskripsi = db.Column(db.Text)
    gambar = db.Column(db.String(255))  # path to image
    status = db.Column(db.String(20), default='tersedia')  # tersedia, tidak_tersedia
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    variants = db.relationship('ProductVariant', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.nama}>'


class ProductVariant(db.Model):
    """Product variant model (size, flavor, etc.)"""
    __tablename__ = 'product_variants'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)  # Variant name/flavor
    ukuran = db.Column(db.String(100))  # Size
    harga = db.Column(db.Numeric(12, 2), nullable=False)
    stok = db.Column(db.Integer, default=0)
    satuan = db.Column(db.String(20), default='pcs')  # unit: pcs, kg, liter, etc.
    gambar = db.Column(db.String(255))  # path to variant image
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='variant', lazy='dynamic')
    stock_movements = db.relationship('StockMovement', backref='variant', lazy='dynamic')
    
    def __repr__(self):
        return f'<ProductVariant {self.nama} - {self.ukuran}>'


class ProductImage(db.Model):
    """Additional product images model"""
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    urutan = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    nomor_invoice = db.Column(db.String(30), unique=True, nullable=False, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True)
    nama_pemesan = db.Column(db.String(100), nullable=False)
    email_pemesan = db.Column(db.String(100))
    phone_pemesan = db.Column(db.String(20), nullable=False)
    metode_pembayaran = db.Column(db.String(50), nullable=False)  # transfer_bank, e_wallet, cash
    total_harga = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(50), default='menunggu_pembayaran')
    # menunggu_pembayaran, menunggu_verifikasi, lunas, diproses, siap_diambil, selesai, dibatalkan
    catatan = db.Column(db.Text)
    kasir_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    member = db.relationship('Member', backref='orders')
    kasir = db.relationship('User', backref='orders')
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.nomor_invoice}>'


class OrderItem(db.Model):
    """Order item model (products in an order)"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=True)
    qty = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Numeric(12, 2), nullable=False)  # Price at time of order
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'


class Payment(db.Model):
    """Payment model"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    metode_pembayaran = db.Column(db.String(50), nullable=False)
    bukti_transfer = db.Column(db.String(255))  # path to transfer proof image
    status = db.Column(db.String(50), default='pending')  # pending, verified, rejected
    diverifikasi_oleh = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    diverifikasi_at = db.Column(db.DateTime)
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    verifikator = db.relationship('User', backref='payment_verifications')
    
    def __repr__(self):
        return f'<Payment {self.id}>'


class MemberPoints(db.Model):
    """Member points history model"""
    __tablename__ = 'member_points'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    poin = db.Column(db.Integer, nullable=False)
    tipe = db.Column(db.String(50), default='earned')  # earned, redeemed, adjusted
    keterangan = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    member = db.relationship('Member', backref='point_history')
    order = db.relationship('Order')


class Reward(db.Model):
    """Reward model for member rewards"""
    __tablename__ = 'rewards'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    poin_dibutuhkan = db.Column(db.Integer, nullable=False)
    gambar = db.Column(db.String(255))
    stok = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    redemptions = db.relationship('RewardRedemption', backref='reward', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Reward {self.nama}>'


class RewardRedemption(db.Model):
    """Reward redemption history model"""
    __tablename__ = 'reward_redemptions'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'), nullable=False)
    poin_digunakan = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, completed, cancelled
    tanggal_pengambilan = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    member = db.relationship('Member', backref='reward_redemptions')
    
    def __repr__(self):
        return f'<RewardRedemption {self.id}>'


class StockMovement(db.Model):
    """Stock movement history model"""
    __tablename__ = 'stock_movements'
    
    id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=False)
    tipe = db.Column(db.String(50), nullable=False)  # in (pembelian), out (penjualan), adjustment
    qty = db.Column(db.Integer, nullable=False)
    keterangan = db.Column(db.String(200))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order = db.relationship('Order')
    creator = db.relationship('User')


class Banner(db.Model):
    """Promotional banner model"""
    __tablename__ = 'banners'
    
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text)
    gambar = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))  # Optional link
    urutan = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Banner {self.judul}>'


class Setting(db.Model):
    """System settings model"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=False)
    tipe = db.Column(db.String(50), default='string')  # string, integer, boolean, json
    deskripsi = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ActivityLog(db.Model):
    """Activity log model for auditing"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # create, update, delete, login, etc.
    entity_type = db.Column(db.String(100))  # product, order, payment, etc.
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # JSON details
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref='activity_logs')


class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True)
    judul = db.Column(db.String(150), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    tipe = db.Column(db.String(50), default='info')  # info, warning, success, error
    dibaca = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='notifications')
    member = db.relationship('Member', backref='notifications')


# =============================================================================
# AUTHENTICATION DECORATORS
# =============================================================================

def login_required(f):
    """Decorator for routes that require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator for routes that require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu', 'error')
            return redirect(url_for('admin_login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Anda tidak memiliki akses ke halaman ini', 'error')
            return redirect(url_for('customer_home'))
        return f(*args, **kwargs)
    return decorated_function


def cashier_required(f):
    """Decorator for routes that require cashier role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu', 'error')
            return redirect(url_for('admin_login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role not in ['admin', 'cashier']:
            flash('Anda tidak memiliki akses ke halaman ini', 'error')
            return redirect(url_for('customer_home'))
        return f(*args, **kwargs)
    return decorated_function


def member_login_required(f):
    """Decorator for routes that require member login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'member_id' not in session:
            flash('Silakan login sebagai member terlebih dahulu', 'error')
            return redirect(url_for('member_login'))
        return f(*args, **kwargs)
    return decorated_function


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_picture(file, folder='products'):
    """Save uploaded picture and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Save to writable/uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Resize image if needed
        img = Image.open(file)
        img.thumbnail((1200, 1200))
        img.save(filepath)
        
        return os.path.join(folder, filename)
    return None


def generate_invoice_number():
    """Generate unique invoice number"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(secrets.choice(string.digits) for _ in range(4))
    return f'INV-{timestamp}-{random_suffix}'


def generate_member_code():
    """Generate unique member code"""
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    random_suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f'MBR-{timestamp}-{random_suffix}'


def format_currency(value):
    """Format currency for display"""
    try:
        return f"Rp {float(value):,.0f}".replace(',', '.')
    except:
        return "Rp 0"


def get_sales_summary(days=30):
    """Get sales summary for last N days"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    total_sales = db.session.query(
        func.sum(Order.total_harga)
    ).filter(
        Order.created_at >= start_date,
        Order.status.in_(['lunas', 'diproses', 'siap_diambil', 'selesai'])
    ).scalar() or 0
    
    total_orders = Order.query.filter(
        Order.created_at >= start_date,
        Order.status.in_(['lunas', 'diproses', 'siap_diambil', 'selesai'])
    ).count()
    
    return {
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'avg_order': float(total_sales) / total_orders if total_orders > 0 else 0
    }


# =============================================================================
# ADMIN ROUTES
# =============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log activity
            log = ActivityLog(
                user_id=user.id,
                action='login',
                entity_type='user',
                entity_id=user.id,
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f'Selamat datang, {user.nama}!', 'success')
            
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('cashier_dashboard'))
        else:
            flash('Username atau password salah', 'error')
    
    return render_template('admin/login.html')


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    user = User.query.get(session['user_id'])
    
    # Get statistics
    total_products = Product.query.count()
    total_variants = ProductVariant.query.count()
    total_orders = Order.query.count()
    total_customers = Member.query.count()
    
    # Sales summary
    sales_30days = get_sales_summary(30)
    sales_today = get_sales_summary(0)
    
    # Recent orders
    recent_orders = Order.query.order_by(desc(Order.created_at)).limit(5).all()
    
    # Low stock products
    low_stock = ProductVariant.query.filter(ProductVariant.stok < 5).all()
    
    # Best selling products
    best_sellers = db.session.query(
        Product.nama,
        func.sum(OrderItem.qty).label('total_qty')
    ).join(OrderItem).join(Order).filter(
        Order.status.in_(['lunas', 'diproses', 'siap_diambil', 'selesai'])
    ).group_by(Product.id).order_by(desc('total_qty')).limit(5).all()
    
    return render_template('admin/dashboard.html',
        user=user,
        total_products=total_products,
        total_variants=total_variants,
        total_orders=total_orders,
        total_customers=total_customers,
        sales_30days=sales_30days,
        sales_today=sales_today,
        recent_orders=recent_orders,
        low_stock=low_stock,
        best_sellers=best_sellers
    )


@app.route('/admin/products')
@admin_required
def admin_products():
    """Product management page"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10)
    categories = Category.query.all()
    
    return render_template('admin/products.html',
        products=products,
        categories=categories
    )


@app.route('/admin/products/create', methods=['GET', 'POST'])
@admin_required
def admin_create_product():
    """Create new product"""
    if request.method == 'POST':
        try:
            nama = request.form.get('nama')
            category_id = request.form.get('category_id', type=int)
            deskripsi = request.form.get('deskripsi')
            gambar_file = request.files.get('gambar')
            
            # Validate input
            if not nama or not category_id:
                return jsonify({'success': False, 'message': 'Nama dan kategori harus diisi'}), 400
            
            # Save image
            gambar = None
            if gambar_file:
                gambar = save_picture(gambar_file, 'products')
            
            product = Product(
                nama=nama,
                category_id=category_id,
                deskripsi=deskripsi,
                gambar=gambar
            )
            
            db.session.add(product)
            db.session.commit()
            
            # Log activity
            log = ActivityLog(
                user_id=session['user_id'],
                action='create',
                entity_type='product',
                entity_id=product.id,
                details=f'Created product: {nama}'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Produk berhasil ditambahkan'}), 201
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    categories = Category.query.all()
    return render_template('admin/create_product.html', categories=categories)


@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            product.nama = request.form.get('nama')
            product.category_id = request.form.get('category_id', type=int)
            product.deskripsi = request.form.get('deskripsi')
            product.status = request.form.get('status', 'tersedia')
            
            # Handle image update
            if 'gambar' in request.files and request.files['gambar']:
                new_gambar = save_picture(request.files['gambar'], 'products')
                if new_gambar:
                    product.gambar = new_gambar
            
            db.session.commit()
            
            # Log activity
            log = ActivityLog(
                user_id=session['user_id'],
                action='update',
                entity_type='product',
                entity_id=product.id,
                details=f'Updated product: {product.nama}'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Produk berhasil diubah'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)


@app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    
    try:
        nama_produk = product.nama
        db.session.delete(product)
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='delete',
            entity_type='product',
            entity_id=product_id,
            details=f'Deleted product: {nama_produk}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Produk berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/variants')
@admin_required
def admin_variants():
    """Variant management page"""
    page = request.args.get('page', 1, type=int)
    variants = ProductVariant.query.paginate(page=page, per_page=10)
    products = Product.query.all()
    
    return render_template('admin/variants.html',
        variants=variants,
        products=products
    )


@app.route('/admin/categories')
@admin_required
def admin_categories():
    """Category management page"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@app.route('/admin/categories/create', methods=['POST'])
@admin_required
def admin_create_category():
    """Create new category"""
    try:
        nama = request.form.get('nama')
        deskripsi = request.form.get('deskripsi')
        
        if not nama:
            return jsonify({'success': False, 'message': 'Nama kategori harus diisi'}), 400
        
        category = Category(nama=nama, deskripsi=deskripsi)
        db.session.add(category)
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='create',
            entity_type='category',
            entity_id=category.id,
            details=f'Created category: {nama}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Kategori berhasil ditambahkan'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Order management page"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(desc(Order.created_at)).paginate(page=page, per_page=10)
    
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter)


@app.route('/admin/orders/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """Order detail page"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@app.route('/admin/members')
@admin_required
def admin_members():
    """Member management page"""
    page = request.args.get('page', 1, type=int)
    members = Member.query.paginate(page=page, per_page=10)
    
    return render_template('admin/members.html', members=members)


@app.route('/admin/rewards')
@admin_required
def admin_rewards():
    """Reward management page"""
    rewards = Reward.query.all()
    return render_template('admin/rewards.html', rewards=rewards)


@app.route('/admin/rewards/create', methods=['POST'])
@admin_required
def admin_create_reward():
    """Create new reward"""
    try:
        nama = request.form.get('nama')
        deskripsi = request.form.get('deskripsi')
        poin_dibutuhkan = request.form.get('poin_dibutuhkan', type=int)
        stok = request.form.get('stok', type=int)
        
        if not nama or not poin_dibutuhkan:
            return jsonify({'success': False, 'message': 'Nama dan poin dibutuhkan harus diisi'}), 400
        
        reward = Reward(
            nama=nama,
            deskripsi=deskripsi,
            poin_dibutuhkan=poin_dibutuhkan,
            stok=stok
        )
        db.session.add(reward)
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='create',
            entity_type='reward',
            entity_id=reward.id,
            details=f'Created reward: {nama}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Reward berhasil ditambahkan'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/banners')
@admin_required
def admin_banners():
    """Banner management page"""
    banners = Banner.query.all()
    return render_template('admin/banners.html', banners=banners)


@app.route('/admin/banners/create', methods=['POST'])
@admin_required
def admin_create_banner():
    """Create new banner"""
    try:
        judul = request.form.get('judul')
        deskripsi = request.form.get('deskripsi')
        link = request.form.get('link')
        gambar_file = request.files.get('gambar')
        
        if not judul or not gambar_file:
            return jsonify({'success': False, 'message': 'Judul dan gambar harus diisi'}), 400
        
        gambar = save_picture(gambar_file, 'banners')
        
        banner = Banner(
            judul=judul,
            deskripsi=deskripsi,
            gambar=gambar,
            link=link
        )
        db.session.add(banner)
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='create',
            entity_type='banner',
            entity_id=banner.id,
            details=f'Created banner: {judul}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Banner berhasil ditambahkan'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/database')
@admin_required
def admin_database():
    """Database management page"""
    db_path = 'pusat_sembako.db'
    db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    
    return render_template('admin/database.html', db_size=db_size)


@app.route('/admin/database/backup')
@admin_required
def admin_database_backup():
    """Backup database"""
    try:
        db_path = 'pusat_sembako.db'
        if os.path.exists(db_path):
            backup_filename = f'pusat_sembako_backup_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.db'
            backup_path = os.path.join('writable/uploads', backup_filename)
            
            shutil.copy2(db_path, backup_path)
            
            # Log activity
            log = ActivityLog(
                user_id=session['user_id'],
                action='backup',
                entity_type='database',
                details=f'Database backup created: {backup_filename}'
            )
            db.session.add(log)
            db.session.commit()
            
            return send_file(backup_path, as_attachment=True, download_name=backup_filename)
        else:
            return jsonify({'success': False, 'message': 'Database file tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/database/restore', methods=['POST'])
@admin_required
def admin_database_restore():
    """Restore database from file"""
    try:
        db_file = request.files.get('database_file')
        
        if not db_file or not db_file.filename.endswith('.db'):
            return jsonify({'success': False, 'message': 'File harus berformat .db'}), 400
        
        # Create backup of current database
        db_path = 'pusat_sembako.db'
        if os.path.exists(db_path):
            backup_path = f'{db_path}.backup_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
            shutil.copy2(db_path, backup_path)
        
        # Replace database with new file
        db_file.save(db_path)
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='restore',
            entity_type='database',
            details=f'Database restored from: {db_file.filename}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Database berhasil di-restore'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/settings')
@admin_required
def admin_settings():
    """System settings page"""
    return render_template('admin/settings.html')


@app.route('/admin/activity-logs')
@admin_required
def admin_activity_logs():
    """Activity logs page"""
    page = request.args.get('page', 1, type=int)
    logs = ActivityLog.query.order_by(desc(ActivityLog.created_at)).paginate(page=page, per_page=20)
    
    return render_template('admin/activity_logs.html', logs=logs)


@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    # Log activity
    log = ActivityLog(
        user_id=session['user_id'],
        action='logout',
        entity_type='user'
    )
    db.session.add(log)
    db.session.commit()
    
    session.clear()
    flash('Anda telah logout', 'success')
    return redirect(url_for('admin_login'))


# =============================================================================
# CASHIER ROUTES
# =============================================================================

@app.route('/cashier/dashboard')
@cashier_required
def cashier_dashboard():
    """Cashier dashboard"""
    user = User.query.get(session['user_id'])
    
    # Get pending orders
    pending_orders = Order.query.filter_by(status='menunggu_verifikasi').all()
    today_orders = Order.query.filter(
        func.date(Order.created_at) == datetime.utcnow().date()
    ).all()
    
    return render_template('cashier/dashboard.html',
        user=user,
        pending_orders=pending_orders,
        today_orders=today_orders
    )


@app.route('/cashier/orders')
@cashier_required
def cashier_orders():
    """Cashier orders page"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'menunggu_verifikasi')
    
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(desc(Order.created_at)).paginate(page=page, per_page=10)
    
    return render_template('cashier/orders.html', orders=orders, status_filter=status_filter)


@app.route('/cashier/orders/<int:order_id>')
@cashier_required
def cashier_order_detail(order_id):
    """Cashier order detail and verification page"""
    order = Order.query.get_or_404(order_id)
    return render_template('cashier/order_detail.html', order=order)


@app.route('/cashier/orders/<int:order_id>/verify-payment', methods=['POST'])
@cashier_required
def cashier_verify_payment(order_id):
    """Verify payment"""
    try:
        order = Order.query.get_or_404(order_id)
        action = request.form.get('action')  # verify or reject
        catatan = request.form.get('catatan', '')
        
        if not order.payment:
            return jsonify({'success': False, 'message': 'Data pembayaran tidak ditemukan'}), 404
        
        if action == 'verify':
            order.payment.status = 'verified'
            order.payment.diverifikasi_oleh = session['user_id']
            order.payment.diverifikasi_at = datetime.utcnow()
            order.payment.catatan = catatan
            order.status = 'lunas'
            
            # Add member points if member
            if order.member_id:
                points = int(float(order.total_harga) * 0.01)  # 1% points
                order.member.points += points
                
                point_log = MemberPoints(
                    member_id=order.member_id,
                    order_id=order.id,
                    poin=points,
                    tipe='earned',
                    keterangan=f'Pembelian {order.nomor_invoice}'
                )
                db.session.add(point_log)
            
            message = 'Pembayaran berhasil diverifikasi'
        elif action == 'reject':
            order.payment.status = 'rejected'
            order.payment.diverifikasi_oleh = session['user_id']
            order.payment.diverifikasi_at = datetime.utcnow()
            order.payment.catatan = catatan
            order.status = 'dibatalkan'
            message = 'Pembayaran ditolak'
        else:
            return jsonify({'success': False, 'message': 'Action tidak valid'}), 400
        
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='verify_payment',
            entity_type='payment',
            entity_id=order.payment.id,
            details=f'Payment {action}: {order.nomor_invoice}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': message}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/cashier/orders/<int:order_id>/update-status', methods=['POST'])
@cashier_required
def cashier_update_order_status(order_id):
    """Update order status"""
    try:
        order = Order.query.get_or_404(order_id)
        new_status = request.form.get('status')
        catatan = request.form.get('catatan', '')
        
        valid_statuses = ['menunggu_pembayaran', 'menunggu_verifikasi', 'lunas', 'diproses', 'siap_diambil', 'selesai', 'dibatalkan']
        if new_status not in valid_statuses:
            return jsonify({'success': False, 'message': 'Status tidak valid'}), 400
        
        old_status = order.status
        order.status = new_status
        order.kasir_id = session['user_id']
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=session['user_id'],
            action='update_status',
            entity_type='order',
            entity_id=order.id,
            details=f'Order status changed from {old_status} to {new_status}'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Status pesanan berhasil diubah'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/cashier/orders/<int:order_id>/invoice')
@cashier_required
def cashier_print_invoice(order_id):
    """Print invoice (placeholder - will be implemented with template)"""
    order = Order.query.get_or_404(order_id)
    return render_template('cashier/invoice.html', order=order)


@app.route('/cashier/logout')
@login_required
def cashier_logout():
    """Cashier logout"""
    # Log activity
    log = ActivityLog(
        user_id=session['user_id'],
        action='logout',
        entity_type='user'
    )
    db.session.add(log)
    db.session.commit()
    
    session.clear()
    flash('Anda telah logout', 'success')
    return redirect(url_for('admin_login'))


# =============================================================================
# CUSTOMER ROUTES
# =============================================================================

@app.route('/')
def customer_home():
    """Customer home page"""
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.urutan).all()
    categories = Category.query.filter_by(is_active=True).all()
    products = Product.query.filter_by(is_active=True).order_by(desc(Product.created_at)).limit(12).all()
    
    return render_template('customer/home.html',
        banners=banners,
        categories=categories,
        products=products
    )


@app.route('/products')
def customer_products():
    """Product catalog page"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')  # newest, popular
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            or_(
                Product.nama.ilike(f'%{search}%'),
                Product.deskripsi.ilike(f'%{search}%')
            )
        )
    
    if sort == 'popular':
        # Get products with most orders
        query = query.outerjoin(OrderItem).group_by(Product.id).order_by(desc(func.count(OrderItem.id)))
    else:
        query = query.order_by(desc(Product.created_at))
    
    products = query.paginate(page=page, per_page=12)
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('customer/products.html',
        products=products,
        categories=categories,
        category_id=category_id,
        search=search,
        sort=sort
    )


@app.route('/products/search')
def customer_search_products():
    """Real-time product search"""
    search = request.args.get('q', '')
    
    if len(search) < 2:
        return jsonify([]), 200
    
    products = Product.query.filter(
        Product.is_active == True,
        or_(
            Product.nama.ilike(f'%{search}%'),
            Product.category.has(Category.nama.ilike(f'%{search}%'))
        )
    ).limit(10).all()
    
    result = [
        {
            'id': p.id,
            'nama': p.nama,
            'category': p.category.nama if p.category else '',
            'image': p.gambar,
            'url': url_for('customer_product_detail', product_id=p.id)
        }
        for p in products
    ]
    
    return jsonify(result), 200


@app.route('/products/<int:product_id>')
def customer_product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    variants = product.variants.filter_by(is_active=True).all()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(6).all()
    
    return render_template('customer/product_detail.html',
        product=product,
        variants=variants,
        related_products=related_products
    )


@app.route('/cart')
def customer_cart():
    """Shopping cart page"""
    cart = session.get('cart', [])
    total = 0
    cart_items = []
    
    for item in cart:
        variant = ProductVariant.query.get(item['variant_id'])
        if variant:
            subtotal = float(variant.harga) * item['qty']
            total += subtotal
            cart_items.append({
                'variant': variant,
                'qty': item['qty'],
                'subtotal': subtotal
            })
    
    return render_template('customer/cart.html', cart_items=cart_items, total=total)


@app.route('/cart/add', methods=['POST'])
def customer_add_to_cart():
    """Add product to cart"""
    try:
        variant_id = request.form.get('variant_id', type=int)
        qty = request.form.get('qty', type=int)
        
        if not variant_id or qty < 1:
            return jsonify({'success': False, 'message': 'Invalid input'}), 400
        
        variant = ProductVariant.query.get_or_404(variant_id)
        
        if variant.stok < qty:
            return jsonify({'success': False, 'message': 'Stok tidak cukup'}), 400
        
        cart = session.get('cart', [])
        
        # Check if item already in cart
        existing_item = next((item for item in cart if item['variant_id'] == variant_id), None)
        if existing_item:
            existing_item['qty'] += qty
        else:
            cart.append({'variant_id': variant_id, 'qty': qty})
        
        session['cart'] = cart
        session.modified = True
        
        return jsonify({'success': True, 'message': 'Produk berhasil ditambahkan ke keranjang', 'cart_count': len(cart)}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/cart/update', methods=['POST'])
def customer_update_cart():
    """Update cart item quantity"""
    try:
        variant_id = request.form.get('variant_id', type=int)
        qty = request.form.get('qty', type=int)
        
        cart = session.get('cart', [])
        item = next((item for item in cart if item['variant_id'] == variant_id), None)
        
        if item:
            if qty <= 0:
                cart.remove(item)
            else:
                variant = ProductVariant.query.get(variant_id)
                if variant.stok < qty:
                    return jsonify({'success': False, 'message': 'Stok tidak cukup'}), 400
                item['qty'] = qty
        
        session['cart'] = cart
        session.modified = True
        
        return jsonify({'success': True, 'message': 'Keranjang berhasil diperbarui'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/cart/remove', methods=['POST'])
def customer_remove_from_cart():
    """Remove item from cart"""
    try:
        variant_id = request.form.get('variant_id', type=int)
        
        cart = session.get('cart', [])
        cart = [item for item in cart if item['variant_id'] != variant_id]
        
        session['cart'] = cart
        session.modified = True
        
        return jsonify({'success': True, 'message': 'Produk berhasil dihapus dari keranjang'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/cart/clear', methods=['POST'])
def customer_clear_cart():
    """Clear entire cart"""
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True, 'message': 'Keranjang berhasil dikosongkan'}), 200


@app.route('/checkout', methods=['GET', 'POST'])
def customer_checkout():
    """Checkout page"""
    cart = session.get('cart', [])
    
    if not cart:
        flash('Keranjang Anda kosong', 'error')
        return redirect(url_for('customer_cart'))
    
    if request.method == 'POST':
        try:
            # Get form data
            nama_pemesan = request.form.get('nama_pemesan')
            email_pemesan = request.form.get('email_pemesan')
            phone_pemesan = request.form.get('phone_pemesan')
            metode_pembayaran = request.form.get('metode_pembayaran')
            catatan = request.form.get('catatan')
            
            # Validate input
            if not all([nama_pemesan, phone_pemesan, metode_pembayaran]):
                return jsonify({'success': False, 'message': 'Data tidak lengkap'}), 400
            
            # Calculate total
            total_harga = 0
            order_items_data = []
            
            for item in cart:
                variant = ProductVariant.query.get(item['variant_id'])
                if not variant:
                    return jsonify({'success': False, 'message': 'Produk tidak ditemukan'}), 404
                
                if variant.stok < item['qty']:
                    return jsonify({'success': False, 'message': f'Stok {variant.nama} tidak cukup'}), 400
                
                subtotal = float(variant.harga) * item['qty']
                total_harga += subtotal
                order_items_data.append({
                    'product_id': variant.product_id,
                    'variant_id': item['variant_id'],
                    'qty': item['qty'],
                    'harga': float(variant.harga),
                    'subtotal': subtotal
                })
            
            # Create order
            nomor_invoice = generate_invoice_number()
            member_id = None
            
            if 'member_id' in session:
                member_id = session['member_id']
            
            order = Order(
                nomor_invoice=nomor_invoice,
                member_id=member_id,
                nama_pemesan=nama_pemesan,
                email_pemesan=email_pemesan,
                phone_pemesan=phone_pemesan,
                metode_pembayaran=metode_pembayaran,
                total_harga=total_harga,
                catatan=catatan
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Add order items and update stock
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data['product_id'],
                    variant_id=item_data['variant_id'],
                    qty=item_data['qty'],
                    harga=item_data['harga'],
                    subtotal=item_data['subtotal']
                )
                db.session.add(order_item)
                
                # Update stock
                variant = ProductVariant.query.get(item_data['variant_id'])
                variant.stok -= item_data['qty']
                
                # Record stock movement
                stock_move = StockMovement(
                    variant_id=item_data['variant_id'],
                    tipe='out',
                    qty=item_data['qty'],
                    keterangan=f'Penjualan {nomor_invoice}',
                    order_id=order.id
                )
                db.session.add(stock_move)
            
            # Create payment record
            payment = Payment(
                order_id=order.id,
                metode_pembayaran=metode_pembayaran,
                status='pending'
            )
            db.session.add(payment)
            
            # Set initial status based on payment method
            if metode_pembayaran in ['transfer_bank', 'e_wallet']:
                order.status = 'menunggu_verifikasi'
            else:  # cash
                order.status = 'menunggu_pembayaran'
            
            db.session.commit()
            
            # Clear cart
            session['cart'] = []
            session.modified = True
            
            return jsonify({
                'success': True,
                'message': 'Pesanan berhasil dibuat',
                'order_id': order.id,
                'invoice_url': url_for('customer_order_invoice', order_id=order.id)
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # GET request - show checkout form
    cart_items = []
    total = 0
    
    for item in cart:
        variant = ProductVariant.query.get(item['variant_id'])
        if variant:
            subtotal = float(variant.harga) * item['qty']
            total += subtotal
            cart_items.append({
                'variant': variant,
                'qty': item['qty'],
                'subtotal': subtotal
            })
    
    member = None
    if 'member_id' in session:
        member = Member.query.get(session['member_id'])
    
    payment_info = config_data.get('payment_methods', {})
    
    return render_template('customer/checkout.html',
        cart_items=cart_items,
        total=total,
        member=member,
        payment_info=payment_info
    )


@app.route('/orders/<int:order_id>/invoice')
def customer_order_invoice(order_id):
    """Order invoice page"""
    order = Order.query.get_or_404(order_id)
    return render_template('customer/invoice.html', order=order)


@app.route('/orders/<int:order_id>/upload-proof', methods=['POST'])
def customer_upload_payment_proof(order_id):
    """Upload payment proof"""
    try:
        order = Order.query.get_or_404(order_id)
        
        if not order.payment:
            return jsonify({'success': False, 'message': 'Data pembayaran tidak ditemukan'}), 404
        
        bukti_file = request.files.get('bukti_transfer')
        if not bukti_file:
            return jsonify({'success': False, 'message': 'File tidak diunggah'}), 400
        
        if not allowed_file(bukti_file.filename):
            return jsonify({'success': False, 'message': 'Format file tidak didukung'}), 400
        
        # Save image
        filename = save_picture(bukti_file, 'payments')
        
        order.payment.bukti_transfer = filename
        order.status = 'menunggu_verifikasi'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Bukti transfer berhasil diunggah'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/orders')
def customer_orders():
    """Customer orders history"""
    if 'member_id' not in session:
        flash('Silakan login sebagai member untuk melihat riwayat pesanan', 'error')
        return redirect(url_for('member_login'))
    
    page = request.args.get('page', 1, type=int)
    member = Member.query.get(session['member_id'])
    orders = member.orders.order_by(desc(Order.created_at)).paginate(page=page, per_page=10)
    
    return render_template('customer/orders.html', orders=orders, member=member)


@app.route('/orders/<int:order_id>')
def customer_order_detail(order_id):
    """View order detail"""
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission to view this order
    if 'member_id' in session:
        if order.member_id != session['member_id']:
            flash('Anda tidak memiliki akses ke pesanan ini', 'error')
            return redirect(url_for('customer_home'))
    
    return render_template('customer/order_detail.html', order=order)


@app.route('/member/login', methods=['GET', 'POST'])
def member_login():
    """Member login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        member = Member.query.filter_by(username=username, is_active=True).first()
        
        if member and member.check_password(password):
            session['member_id'] = member.id
            session['member_username'] = member.username
            session['member_nama'] = member.nama
            member.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Selamat datang, {member.nama}!', 'success')
            return redirect(url_for('customer_home'))
        else:
            flash('Username atau password salah', 'error')
    
    return render_template('customer/member_login.html')


@app.route('/member/register', methods=['GET', 'POST'])
def member_register():
    """Member registration page"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            nama = request.form.get('nama')
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            # Validate input
            if not all([username, password, nama, email, phone]):
                return jsonify({'success': False, 'message': 'Data tidak lengkap'}), 400
            
            if password != password_confirm:
                return jsonify({'success': False, 'message': 'Password tidak cocok'}), 400
            
            # Check if username/email already exists
            if Member.query.filter_by(username=username).first():
                return jsonify({'success': False, 'message': 'Username sudah digunakan'}), 400
            
            if Member.query.filter_by(email=email).first():
                return jsonify({'success': False, 'message': 'Email sudah terdaftar'}), 400
            
            # Create member
            member_code = generate_member_code()
            member = Member(
                member_code=member_code,
                username=username,
                nama=nama,
                email=email,
                phone=phone
            )
            member.set_password(password)
            
            db.session.add(member)
            db.session.commit()
            
            flash('Akun berhasil dibuat! Silakan login', 'success')
            return redirect(url_for('member_login'))
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return render_template('customer/member_register.html')


@app.route('/member/profile')
@member_login_required
def member_profile():
    """Member profile page"""
    member = Member.query.get(session['member_id'])
    return render_template('customer/member_profile.html', member=member)


@app.route('/member/rewards')
@member_login_required
def member_rewards():
    """Member rewards page"""
    member = Member.query.get(session['member_id'])
    rewards = Reward.query.filter_by(is_active=True).all()
    redemptions = member.reward_redemptions.all()
    
    return render_template('customer/member_rewards.html',
        member=member,
        rewards=rewards,
        redemptions=redemptions
    )


@app.route('/member/redeem-reward', methods=['POST'])
@member_login_required
def member_redeem_reward():
    """Redeem reward"""
    try:
        reward_id = request.form.get('reward_id', type=int)
        member = Member.query.get(session['member_id'])
        reward = Reward.query.get_or_404(reward_id)
        
        if not reward.is_active:
            return jsonify({'success': False, 'message': 'Reward tidak tersedia'}), 400
        
        if member.points < reward.poin_dibutuhkan:
            return jsonify({'success': False, 'message': 'Poin Anda tidak cukup'}), 400
        
        if reward.stok <= 0:
            return jsonify({'success': False, 'message': 'Stok reward habis'}), 400
        
        # Create redemption
        redemption = RewardRedemption(
            member_id=member.id,
            reward_id=reward.id,
            poin_digunakan=reward.poin_dibutuhkan
        )
        
        # Deduct points
        member.points -= reward.poin_dibutuhkan
        reward.stok -= 1
        
        # Log points
        point_log = MemberPoints(
            member_id=member.id,
            poin=-reward.poin_dibutuhkan,
            tipe='redeemed',
            keterangan=f'Penukaran reward: {reward.nama}'
        )
        
        db.session.add(redemption)
        db.session.add(point_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reward berhasil ditukar',
            'remaining_points': member.points
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/member/logout')
def member_logout():
    """Member logout"""
    session.pop('member_id', None)
    session.pop('member_username', None)
    session.pop('member_nama', None)
    session.modified = True
    flash('Anda telah logout', 'success')
    return redirect(url_for('customer_home'))


# =============================================================================
# API ROUTES (JSON responses)
# =============================================================================

@app.route('/api/cart/count')
def api_cart_count():
    """Get cart item count"""
    cart = session.get('cart', [])
    return jsonify({'count': len(cart)}), 200


@app.route('/api/products/<int:product_id>/variants')
def api_product_variants(product_id):
    """Get product variants as JSON"""
    product = Product.query.get_or_404(product_id)
    variants = product.variants.filter_by(is_active=True).all()
    
    result = [
        {
            'id': v.id,
            'nama': v.nama,
            'ukuran': v.ukuran,
            'harga': float(v.harga),
            'stok': v.stok,
            'satuan': v.satuan
        }
        for v in variants
    ]
    
    return jsonify(result), 200


@app.route('/api/categories')
def api_categories():
    """Get all active categories"""
    categories = Category.query.filter_by(is_active=True).all()
    
    result = [
        {
            'id': c.id,
            'nama': c.nama,
            'icon': c.icon
        }
        for c in categories
    ]
    
    return jsonify(result), 200


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    return render_template('errors/403.html'), 403


# =============================================================================
# CLI COMMANDS
# =============================================================================

@app.cli.command()
def init_db():
    """Initialize the database with default data"""
    print('Creating database tables...')
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Role.query.first():
            print('Database already initialized!')
            return
        
        # Create roles
        admin_role = Role(name='admin', description='Administrator')
        cashier_role = Role(name='cashier', description='Cashier')
        customer_role = Role(name='customer', description='Customer')
        
        db.session.add_all([admin_role, cashier_role, customer_role])
        db.session.commit()
        
        # Create default admin user
        admin = User(
            username='admin',
            nama='Administrator',
            email='admin@pusatsembako.com',
            phone='08XX-XXXX-XXXX',
            role='admin'
        )
        admin.set_password('admin123')
        
        # Create default cashier user
        cashier = User(
            username='kasir01',
            nama='Kasir 1',
            email='kasir@pusatsembako.com',
            phone='08XX-XXXX-XXXX',
            role='cashier'
        )
        cashier.set_password('kasir01#123')
        
        db.session.add_all([admin, cashier])
        
        # Create default categories
        categories_data = [
            ('Sembako', 'Kebutuhan pokok sehari-hari'),
            ('Bumbu & Bahan Masakan', 'Bumbu dan bahan untuk masakan'),
            ('Minuman', 'Berbagai jenis minuman'),
            ('Makanan', 'Makanan siap saji dan camilan'),
            ('Snack', 'Makanan ringan dan camilan'),
            ('Kebersihan & Perawatan', 'Produk kebersihan dan perawatan'),
            ('Kebutuhan Rumah Tangga', 'Kebutuhan untuk rumah tangga'),
        ]
        
        for nama, deskripsi in categories_data:
            category = Category(nama=nama, deskripsi=deskripsi, is_active=True)
            db.session.add(category)
        
        db.session.commit()
        
        print('Database initialized successfully!')
        print('Default admin credentials: username=admin, password=admin123')
        print('Default cashier credentials: username=kasir01, password=kasir01#123')


# =============================================================================
# CONTEXT PROCESSORS & FILTERS
# =============================================================================

@app.context_processor
def inject_user():
    """Inject user context to templates"""
    user = None
    member = None
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    if 'member_id' in session:
        member = Member.query.get(session['member_id'])
    
    return {'current_user': user, 'current_member': member, 'format_currency': format_currency}


app.jinja_env.filters['currency'] = format_currency


# =============================================================================
# MAIN APPLICATION ENTRY
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        # Create database and tables if they don't exist
        db.create_all()
        
        # Check if database needs initialization
        if not Role.query.first():
            print('Initializing database with default data...')
            app.cli.commands['init_db'].invoke()
    
    # Determine host and port
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f'\n=== PUSAT SEMBAKO ==="')
    print(f'Starting Flask application on {host}:{port}')
    print(f'Access the application at http://localhost:{port}')
    print(f'Admin Panel: http://localhost:{port}/admin/login')
    print(f'Debug Mode: {debug}\n')
    
    app.run(host=host, port=port, debug=debug, use_reloader=True)
