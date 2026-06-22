# PUSAT SEMBAKO - Sistem Penjualan Sembako

Aplikasi web untuk manajemen penjualan produk sembako dengan fitur Admin, Kasir, dan Pembeli.

## Fitur Utama

### Admin
- Dashboard lengkap dengan statistik penjualan
- Manajemen produk dan kategori
- Manajemen varian produk
- Manajemen stok
- Manajemen kasir dan member
- Manajemen reward dan poin
- Manajemen banner promosi
- Backup dan restore database
- Laporan penjualan

### Kasir
- Melihat pesanan masuk
- Verifikasi bukti transfer pembayaran
- Update status pesanan
- Cetak invoice
- Riwayat transaksi

### Pembeli
- Browsing katalog produk
- Pencarian real-time
- Keranjang belanja
- Checkout dengan berbagai metode pembayaran
- Riwayat pesanan
- Status tracking pesanan
- Program member dan reward

## Teknologi

- **Backend**: Python 3.11 + Flask
- **Database**: SQLite
- **Frontend**: Bootstrap 5 + Jinja2
- **ORM**: SQLAlchemy

## Struktur Folder

```
project-root/
├── app/
│   ├── templates/
│   │   ├── admin/
│   │   ├── cashier/
│   │   ├── customer/
│   │   └── base.html
│   └── static/
│       ├── css/
│       └── js/
├── public/
│   └── assets/
│       ├── products/
│       ├── variants/
│       ├── banners/
│       └── logos/
├── writable/
│   ├── uploads/
│   ├── logs/
│   └── invoices/
├── tests/
├── app.py
├── config.json
├── requirements.txt
├── Dockerfile
├── huggingface.yml
├── .env.example
└── .gitignore
```

## Instalasi

### Windows (Local Development)

1. Clone repository:
```bash
git clone https://github.com/inawatimaulana012/pusatsembako.git
cd pusatsembako
```

2. Buat virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy .env.example ke .env:
```bash
copy .env.example .env
```

5. Jalankan aplikasi:
```bash
python app.py
```

6. Akses di browser:
```
http://localhost:5000
```

## Default Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Kasir
- Username: `kasir01`
- Password: `kasir01#123`

## Deploy ke Hugging Face Spaces

1. Buat Space di Hugging Face (Non-AI)
2. Clone repository Hugging Face Space Anda
3. Copy semua file project ke Space
4. Push ke Hugging Face:
```bash
git add .
git commit -m "Deploy PUSAT SEMBAKO"
git push
```

Aplikasi akan otomatis di-deploy.

## FAQ

### Bisakah saya mengganti database di Hugging Face?
Ya, fitur Backup & Restore Database memungkinkan Anda untuk:
- Download database saat ini
- Upload database baru
- Restore database kapan saja

Fitur ini tersedia di menu Admin > Pengaturan Database.

### Apakah upload gambar berfungsi di Hugging Face?
Ya, upload gambar disimpan di folder `writable/uploads/` yang bersifat persisten di Hugging Face.

### Bagaimana cara menambah produk?
1. Login sebagai Admin
2. Ke menu Kelola Produk
3. Klik Tambah Produk
4. Isi data dan upload gambar
5. Simpan

## Lisensi

MIT License

## Support

Hubungi: info@pusatsembako.com
