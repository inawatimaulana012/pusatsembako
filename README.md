# PUSAT SEMBAKO

Sistem Manajemen Toko Sembako (Grocery Store Management System) berbasis Python Flask.

## Fitur Utama

### Admin
- Dashboard dengan statistik penjualan
- Manajemen produk dan kategori
- Manajemen varian produk
- Manajemen stok
- Manajemen kasir
- Manajemen member dan reward
- Manajemen pesanan dan pembayaran
- Kelola banner dan logo toko
- Backup dan restore database
- Laporan penjualan

### Kasir
- Melihat pesanan masuk
- Verifikasi bukti transfer
- Ubah status pesanan
- Konfirmasi pembayaran
- Cetak invoice
- Riwayat transaksi

### Pembeli
- Lihat katalog produk
- Cari produk real-time
- Keranjang belanja
- Checkout
- Status pesanan
- Riwayat pemesanan
- Member dengan sistem poin dan reward

## Teknologi

- **Backend**: Python 3.11 + Flask
- **Database**: SQLite dengan SQLAlchemy ORM
- **Frontend**: Bootstrap 5 + Jinja2 Templates
- **File Management**: Werkzeug
- **Deployment**: Docker + Gunicorn

## Struktur Folder

```
projekt-root/
├── app/
│   ├── templates/
│   │   ├── admin/
│   │   ├── cashier/
│   │   ├── customer/
│   │   └── auth/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── public/
│   └── assets/
│       ├── products/
│       ├── variants/
│       ├── banners/
│       ├── logos/
│       └── uploads/
├── writable/
│   ├── uploads/
│   └── logs/
├── tests/
├── app.py
├── config.json
├── requirements.txt
├── Dockerfile
├── huggingface.yml
├── .env.example
├── .gitignore
└── README.md
```

## Instalasi Lokal (Windows)

### 1. Clone Repository
```bash
git clone https://github.com/inawatimaulana012/pusatsembako.git
cd pusatsembako
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
copy .env.example .env
```
Edit `.env` dan ubah `SECRET_KEY` dengan nilai unik.

### 5. Buat Folder Diperlukan
```bash
mkdir -p writable\uploads writable\logs
mkdir -p public\assets\products public\assets\variants public\assets\banners public\assets\logos
```

### 6. Jalankan Aplikasi
```bash
python app.py
```

Akses di browser: `http://localhost:5000`

## Akun Default

### Admin
- **Username**: admin
- **Password**: admin123

### Kasir
- **Username**: kasir1
- **Password**: kasir123

## Deploy ke Hugging Face Spaces

### 1. Buat Hugging Face Spaces
- Kunjungi https://huggingface.co/spaces
- Klik "Create new Space"
- Pilih "Docker" sebagai SDK
- Buat space

### 2. Push ke Repository
```bash
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/pusatsembako
git push huggingface main
```

### 3. Tunggu Build
Hugging Face akan otomatis build Docker image dan deploy aplikasi.

## FAQ

### Apakah saya bisa lepas pasang file database di Hugging Face?

**Ya, bisa!** Aplikasi memiliki fitur:
- **Backup Database**: Download file `.db` dari dashboard admin
- **Upload Database Baru**: Upload file `.db` baru dari dashboard admin
- **Restore Database**: Restore backup dari dashboard admin

Untuk production:
1. Backup database regular dari dashboard admin
2. Download dan simpan di tempat aman
3. Jika butuh database baru, upload melalui dashboard admin
4. Restart aplikasi (otomatis di Hugging Face)

### Bagaimana cara upload gambar produk?

Admin dapat upload gambar melalui:
1. Dashboard Admin → Kelola Produk → Upload Foto Produk
2. Dashboard Admin → Kelola Varian → Upload Foto Varian
3. Dashboard Admin → Pengaturan → Upload Logo Toko

Gambar disimpan di `public/assets/` dan `writable/uploads/`

### Apakah support Mobile?

Yes! Bootstrap 5 memastikan responsive di semua ukuran layar.

## Kontribusi

Untuk kontribusi, silakan buat pull request.

## Lisensi

MIT License
