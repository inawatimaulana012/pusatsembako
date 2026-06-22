# MAKALAH LAPORAN SKRIPSI/TUGAS AKHIR
## PUSAT SEMBAKO - Sistem Informasi Penjualan dan Manajemen Inventory

---

## A. PENDAHULUAN

### 1. Latar Belakang

Toko Pusat Sembako merupakan usaha retail yang menjual kebutuhan pokok (sembako) dan produk-produk konsumsi sehari-hari kepada masyarakat. Dengan meningkatnya permintaan konsumen dan jumlah produk yang terus berkembang, pengelolaan bisnis secara manual menjadi semakin sulit dan tidak efisien.

Permasalahan utama yang dihadapi adalah:
- Pencatatan transaksi dan stok masih dilakukan secara manual atau menggunakan spreadsheet sederhana
- Proses verifikasi pembayaran dilakukan secara tidak terstruktur
- Tidak adanya sistem tracking pesanan real-time yang dapat diakses pelanggan
- Manajemen inventory yang tidak terorganisir mengakibatkan sering terjadi kekosongan stok atau overstok
- Tidak tersedia program loyalitas member yang terukur
- Laporan penjualan dan analisis bisnis sulit dilakukan
- Proses checkout dan pemesanan memerlukan interaksi langsung dengan kasir

Oleh karena itu, diperlukan sebuah sistem informasi terintegrasi yang dapat mengelola seluruh aspek bisnis Pusat Sembako mulai dari manajemen produk, inventory, transaksi, hingga hubungan dengan pelanggan.

### 2. Identifikasi Masalah

1. **Sistem Pencatatan Manual**: Transaksi dan stok dicatat secara manual menggunakan buku atau spreadsheet, sehingga rawan terjadi kesalahan dan kehilangan data.

2. **Tidak Ada Sistem Verifikasi Pembayaran**: Verifikasi pembayaran transfer dilakukan secara manual tanpa sistem tracking yang jelas.

3. **Pelanggan Tidak Dapat Melacak Pesanan**: Pelanggan tidak memiliki akses untuk mengetahui status pesanan mereka secara real-time.

4. **Manajemen Stok yang Tidak Efisien**: Tidak ada sistem otomatis untuk monitoring stok, sehingga sering terjadi mismatch antara stok fisik dan pencatatan.

5. **Tidak Ada Program Member dan Reward**: Belum ada sistem untuk memberikan reward atau insentif kepada pelanggan setia.

6. **Laporan dan Analisis Bisnis Terbatas**: Sulit untuk mendapatkan insight bisnis karena tidak ada sistem reporting yang terintegrasi.

7. **Proses Bisnis yang Tidak Terkoneksi**: Berbagai proses bisnis (penjualan, pembayaran, inventory) tidak terintegrasi satu sama lain.

### 3. Perumusan Masalah

Bagaimana membangun sebuah sistem informasi terintegrasi untuk Pusat Sembako yang dapat:

1. Mengelola data produk dan varian produk dengan efisien?
2. Mengotomasi proses transaksi dan verifikasi pembayaran?
3. Menyediakan akses real-time bagi pelanggan untuk melacak status pesanan?
4. Mengoptimalkan manajemen inventory dan stok?
5. Mengimplementasikan program member dan reward system?
6. Menghasilkan laporan dan analisis penjualan yang akurat?
7. Meningkatkan efisiensi operasional dan pengalaman pelanggan?

### 4. Tujuan Penelitian

1. Menganalisis kebutuhan sistem informasi untuk Pusat Sembako
2. Merancang arsitektur sistem informasi yang terintegrasi
3. Mengembangkan aplikasi web untuk manajemen penjualan dan inventory
4. Mengimplementasikan fitur-fitur yang mendukung operasional bisnis
5. Melakukan testing dan deployment aplikasi
6. Memberikan solusi yang dapat meningkatkan efisiensi dan profitabilitas toko

### 5. Manfaat Penelitian

**Manfaat Teoritis:**
- Berkontribusi pada pengembangan ilmu sistem informasi khususnya di bidang e-commerce dan manajemen retail
- Menjadi referensi untuk penelitian serupa di bidang UMKM dan retail

**Manfaat Praktis:**
- Meningkatkan efisiensi operasional Pusat Sembako
- Memberikan pengalaman berbelanja yang lebih baik kepada pelanggan
- Memfasilitasi ekspansi bisnis dengan infrastruktur sistem yang solid
- Menyediakan data akurat untuk decision making

### 6. Batasan Masalah

1. Sistem hanya fokus pada layanan take-away/ambil sendiri, tidak termasuk pengiriman
2. Metode pembayaran terbatas pada transfer bank, e-wallet, dan cash
3. Sistem dirancang untuk satu lokasi toko (single-store)
4. Frontend hanya untuk desktop dan mobile responsif (bukan aplikasi native)
5. Tidak menggunakan machine learning atau AI advanced
6. Database menggunakan SQLite (dapat ditingkatkan ke PostgreSQL jika diperlukan scalability lebih tinggi)

---

## B. TINJAUAN PUSTAKA

### 1. Teori Pendukung

#### A. Sistem Informasi
**Definisi**: Sistem informasi adalah kumpulan komponen-komponen terkait yang berfungsi mengumpulkan (input), memproses (process), dan mengirimkan hasil informasi (output) untuk mendukung pengambilan keputusan dan kendali dalam organisasi.

**Teori Relevan**:
- Teori Sistem Informasi (Laudon & Laudon, 2016)
- Konsep SDLC (System Development Life Cycle)
- Konsep Database Management System

**Referensi**:
- Laudon, K. C., & Laudon, J. P. (2016). Management Information Systems: Managing the Digital Firm (14th ed.). Pearson.

#### B. E-Commerce
**Definisi**: E-Commerce adalah proses pembelian, penjualan, transfer, atau pertukaran produk, layanan, atau informasi melalui jaringan komputer, terutama internet.

**Teori Relevan**:
- E-Commerce Models dan Architecture
- Digital Payment Systems
- Customer Relationship Management (CRM)
- Online Transaction Processing

**Referensi**:
- Chaffey, D., & Ellis-Chadwick, F. (2019). Digital Marketing: Strategy, Implementation and Practice (6th ed.). Pearson.
- Turban, E., Outland, J., Heines, D., & Liang, T. P. (2017). Electronic Commerce: A Managerial and Social Networks Perspective (9th ed.). Springer.

#### C. Manajemen Inventory
**Definisi**: Inventory management adalah proses mengatur pergerakan dan penyimpanan barang dalam organisasi dari supplier hingga customer.

**Teori Relevan**:
- Economic Order Quantity (EOQ)
- Just-In-Time (JIT) Inventory System
- Inventory Turnover Ratio
- Stock Control Methods

**Referensi**:
- Heizer, J., Render, B., & Munson, C. (2016). Operations Management: Sustainability and Supply Chain Management (12th ed.). Pearson.

#### D. User Interface dan User Experience (UI/UX)
**Definisi**: UI/UX merujuk pada desain dan pengalaman pengguna dalam berinteraksi dengan aplikasi atau website.

**Teori Relevan**:
- Design Principles (Gestalt, Minimalism, Consistency)
- Usability Testing
- Responsive Design
- Mobile-First Design Approach

**Referensi**:
- Norman, D. A. (2013). The Design of Everyday Things: Revised and Expanded Edition. Basic Books.
- Nielsen, J. (2000). Designing Web Usability. New Riders.

#### E. Database Design
**Definisi**: Database design adalah proses merencanakan struktur database yang optimal untuk menyimpan dan mengelola data.

**Teori Relevan**:
- Normalisasi Database (1NF, 2NF, 3NF, BCNF)
- Entity-Relationship Model (ER Model)
- SQL dan Query Optimization
- ACID Properties (Atomicity, Consistency, Isolation, Durability)

**Referensi**:
- Date, C. J. (2015). An Introduction to Database Systems (10th ed.). Pearson.
- Ramakrishnan, R., & Gehrke, J. (2003). Database Management Systems (3rd ed.). McGraw-Hill.

#### F. Web Application Architecture
**Definisi**: Web application architecture adalah struktur teknis yang mendefinisikan cara komponen-komponen aplikasi web berinteraksi satu sama lain.

**Teori Relevan**:
- Model-View-Controller (MVC) Architecture
- Three-Tier Architecture
- Microservices Architecture
- RESTful API Design

**Referensi**:
- Richardson, L., & Ruby, S. (2007). RESTful Web Services. O'Reilly Media.
- Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley.

#### G. Software Security
**Definisi**: Software security adalah praktik mengembangkan, membeli, atau mempertahankan software dengan cara meminimalkan kerentanan keamanan.

**Teori Relevan**:
- Authentication dan Authorization
- Password Hashing dan Encryption
- SQL Injection Prevention
- OWASP Top 10 Vulnerabilities

**Referensi**:
- McGraw, G. (2006). Software Security: Building Security In. Addison-Wesley.
- OWASP Foundation. (2021). OWASP Top 10. https://owasp.org/Top10/

### 2. Peralatan dan Teknologi Pendukung

#### Backend & Framework
- **Python 3.11**: Bahasa pemrograman yang powerful dan readable
- **Flask**: Micro web framework yang ringan dan fleksibel
- **SQLAlchemy**: ORM (Object-Relational Mapping) untuk manajemen database

#### Frontend & UI
- **HTML5**: Markup language untuk struktur halaman web
- **CSS3**: Stylesheet language untuk styling
- **Bootstrap 5**: Frontend framework untuk responsive design
- **Jinja2**: Template engine untuk dynamic HTML rendering
- **JavaScript**: Client-side scripting untuk interaktivitas

#### Database
- **SQLite**: Lightweight relational database
- **SQL**: Structured Query Language untuk query database

#### Development Tools
- **Git & GitHub**: Version control dan repository hosting
- **Visual Studio Code**: Code editor
- **Postman**: API testing tool
- **DevTools Browser**: Debugging frontend

#### Deployment & Infrastructure
- **Docker**: Containerization platform
- **Hugging Face Spaces**: Cloud hosting platform untuk deployment
- **GitHub Actions**: CI/CD automation (optional)

#### Supporting Tools
- **Pillow (PIL)**: Image processing library
- **python-dotenv**: Environment variable management
- **pytz**: Timezone handling
- **Werkzeug**: WSGI utility library

---

## C. TINJAUAN INSTITUSI/ORGANISASI

### 1. Profil Institusi

**Nama**: Pusat Sembako
**Jenis Usaha**: Retail - Penjualan Kebutuhan Pokok dan Produk Konsumsi Harian
**Skala Usaha**: UMKM (Usaha Mikro, Kecil, Menengah)
**Lokasi**: [Disesuaikan dengan lokasi actual]
**Tahun Berdiri**: [Disesuaikan dengan data actual]

### 2. Sejarah dan Perkembangan

[Bagian ini disesuaikan dengan data historis actual dari Pusat Sembako - Contoh struktur]

- **Periode Awal (Tahun X-Y)**: Deskripsi tentang bagaimana bisnis dimulai, latar belakang pendirian, produk awal
- **Periode Pertumbuhan (Tahun X-Y)**: Ekspansi produk, peningkatan omset penjualan, penambahan karyawan
- **Periode Saat Ini**: Status bisnis current, jumlah karyawan, jumlah produk, target pasar
- **Visi & Misi**: Deskripsi visi dan misi Pusat Sembako

### 3. Struktur Organisasi

```
Pusat Sembako
    |
    ├── Pemilik/Owner
    |   |
    |   ├── Admin/Manajer
    |   |   ├── Staf Inventory
    |   |   └── Staf Keuangan
    |   |
    |   └── Kasir (1-3 orang)
    |       ├── Kasir 1
    |       ├── Kasir 2
    |       └── Kasir 3
    |
    └── Pelanggan
        ├── Member Tetap
        └── Pelanggan Casual
```

### 4. Deskripsi Proses Bisnis Saat Ini

#### A. Proses Penjualan
1. Pelanggan datang ke toko
2. Pelanggan memilih produk
3. Pelanggan membawa produk ke kasir
4. Kasir menghitung total harga secara manual
5. Pelanggan melakukan pembayaran (cash/transfer)
6. Kasir mencatat transaksi di buku atau spreadsheet
7. Pelanggan meninggalkan toko dengan produk

**Masalah**: Proses ini rentan kesalahan hitung, tidak ada tracking pembayaran yang jelas, dan sulit untuk analisis.

#### B. Proses Manajemen Stok
1. Pemilik atau manajer melakukan stock opname secara berkala (manual)
2. Mencatat stok di buku atau spreadsheet
3. Jika stok habis, melakukan pemesanan ke supplier
4. Tidak ada sistem early warning untuk stok yang menipis

**Masalah**: Sering terjadi kekosongan stok yang tidak terduga atau overstok yang merugikan.

#### C. Proses Verifikasi Pembayaran Transfer
1. Pelanggan transfer ke rekening toko
2. Pelanggan manual upload bukti transfer via SMS/WhatsApp/datang langsung
3. Pemilik atau kasir manual verifikasi transfer (bisa terlewat)
4. Tidak ada sistem tracking yang jelas

**Masalah**: Transfer bisa terlewatkan, verifikasi tidak terstruktur, dan sulit untuk reconciliation.

#### D. Proses Manajemen Member
1. Tidak ada sistem member yang formal
2. Pelanggan tetap hanya dikenali secara personal
3. Tidak ada program loyalitas atau reward
4. Sulit untuk retention pelanggan

**Masalah**: Tidak ada data terstruktur tentang pelanggan, sulit untuk targeted marketing.

### 5. Komputerisasi Sistem Pendataan Transaksi dan Stok

#### Sistem Saat Ini (As-Is)
- **Tools**: Microsoft Excel / Google Sheets
- **Struktur Data**: Tabel sederhana dengan kolom tanggal, item, qty, harga, total
- **Limitation**: 
  - Tidak real-time
  - Sulit untuk filtering dan analisis kompleks
  - Rawan data corruption
  - Tidak ada backup otomatis
  - Tidak dapat diakses dari berbagai device/lokasi secara optimal

#### Sistem yang Diharapkan (To-Be)
- **Tools**: Aplikasi Web PUSAT SEMBAKO
- **Struktur Data**: Database relasional yang terstruktur dengan tabel-tabel terkait
- **Features**:
  - Real-time transaction recording
  - Automatic stock tracking dan updating
  - Multi-user access dengan role-based permissions
  - Automated backup dan data integrity checks
  - Accessible dari berbagai device dan lokasi
  - Generating reports dan analytics
  - Integration dengan payment methods

### 6. Analisis Kebutuhan Perangkat Lunak

#### A. Kebutuhan Fungsional (Functional Requirements)

**1. Modul Admin**
- FR-A1: Admin dapat login dengan username dan password
- FR-A2: Admin dapat manage produk (CRUD - Create, Read, Update, Delete)
- FR-A3: Admin dapat manage kategori produk
- FR-A4: Admin dapat manage varian produk dengan harga dan stok
- FR-A5: Admin dapat upload foto produk dan varian
- FR-A6: Admin dapat manage kasir user
- FR-A7: Admin dapat manage member
- FR-A8: Admin dapat manage reward dan poin
- FR-A9: Admin dapat manage banner promosi
- FR-A10: Admin dapat melihat dan manage semua pesanan
- FR-A11: Admin dapat backup dan restore database
- FR-A12: Admin dapat melihat dashboard dengan statistik penjualan
- FR-A13: Admin dapat generate laporan penjualan
- FR-A14: Admin dapat manage pengaturan sistem
- FR-A15: Admin dapat melihat activity log

**2. Modul Kasir**
- FR-K1: Kasir dapat login dengan username dan password
- FR-K2: Kasir dapat melihat pesanan masuk yang menunggu verifikasi
- FR-K3: Kasir dapat verify bukti transfer pembayaran
- FR-K4: Kasir dapat update status pesanan
- FR-K5: Kasir dapat confirm pembayaran
- FR-K6: Kasir dapat print invoice
- FR-K7: Kasir dapat melihat riwayat transaksi hari ini
- FR-K8: Kasir dapat melihat dashboard dengan pesanan pending

**3. Modul Pembeli (Customer)**
- FR-C1: Pembeli dapat browse katalog produk
- FR-C2: Pembeli dapat melihat kategori produk
- FR-C3: Pembeli dapat search produk secara real-time
- FR-C4: Pembeli dapat melihat detail produk dan varian
- FR-C5: Pembeli dapat tambah produk ke keranjang
- FR-C6: Pembeli dapat manage keranjang (edit qty, hapus item)
- FR-C7: Pembeli dapat checkout dan membuat pesanan
- FR-C8: Pembeli dapat pilih metode pembayaran
- FR-C9: Pembeli dapat upload bukti transfer (jika transfer)
- FR-C10: Pembeli dapat melihat invoice setelah checkout
- FR-C11: Pembeli dapat melihat riwayat pesanan (harus login)
- FR-C12: Pembeli dapat track status pesanan
- FR-C13: Pembeli dapat member login/register
- FR-C14: Pembeli dapat melihat poin dan reward yang tersedia
- FR-C15: Pembeli dapat redeem reward dengan poin
- FR-C16: Pembeli dapat guest checkout tanpa member

#### B. Kebutuhan Non-Fungsional (Non-Functional Requirements)

**1. Performance**
- NFR-P1: Waktu response untuk setiap halaman < 2 detik
- NFR-P2: Sistem dapat menangani minimal 100 concurrent users
- NFR-P3: Database query harus optimal dengan index yang tepat

**2. Security**
- NFR-S1: Password harus di-hash menggunakan algoritma yang aman (bcrypt)
- NFR-S2: Session harus ter-manage dengan baik (timeout setelah 30 menit inactivity)
- NFR-S3: File upload harus divalidasi (type, size, malware scanning)
- NFR-S4: SQL Injection dan XSS attacks harus dicegah
- NFR-S5: Data sensitif (password, bukti transfer) harus dienkripsi

**3. Usability**
- NFR-U1: Interface harus intuitif dan mudah digunakan
- NFR-U2: Responsif di desktop, tablet, dan mobile
- NFR-U3: Loading time minimal dan smooth animations
- NFR-U4: Clear error messages dan validations
- NFR-U5: Accessibility features untuk users dengan disabilities

**4. Reliability**
- NFR-R1: Uptime minimal 99%
- NFR-R2: Automatic backup setiap hari
- NFR-R3: Data recovery system dalam case of failure
- NFR-R4: Error logging dan monitoring

**5. Scalability**
- NFR-SC1: Sistem dapat scale jika jumlah produk bertambah
- NFR-SC2: Database dapat handle pertumbuhan data dalam 2-3 tahun ke depan
- NFR-SC3: Dapat upgrade dari SQLite ke PostgreSQL jika diperlukan

**6. Compatibility**
- NFR-C1: Kompatibel dengan Windows 10/11
- NFR-C2: Kompatibel dengan browser modern (Chrome, Firefox, Safari, Edge)
- NFR-C3: Kompatibel dengan mobile browsers
- NFR-C4: Responsive design untuk berbagai screen sizes

**7. Maintainability**
- NFR-M1: Code harus terstruktur dan documented
- NFR-M2: Mudah untuk penambahan fitur di masa depan
- NFR-M3: Clear separation of concerns (MVC pattern)

#### C. Kebutuhan Data

**Data yang Diperlukan**:
1. Data Master: Produk, Kategori, Varian, Member, User, Reward
2. Data Transaksi: Order, Order Items, Payment, Payment Proofs
3. Data Support: Banner, Settings, Activity Log, Stock Movements

#### D. Kebutuhan Hardware

**Untuk Development**:
- Processor: Intel i5 atau equivalent
- RAM: 8GB minimum
- Storage: 256GB SSD
- Network: Internet connection

**Untuk Deployment (Hugging Face Spaces)**:
- Sudah disediakan oleh Hugging Face
- Minimal: 4GB RAM, 50GB Storage

#### E. Kebutuhan Software

**Development Environment**:
- Python 3.11
- Flask framework
- SQLAlchemy ORM
- Git version control
- Visual Studio Code atau text editor lainnya

**Production Environment**:
- Python 3.11
- Flask dengan WSGI server (Gunicorn)
- SQLite database
- Docker (untuk containerization)

---

## KESIMPULAN TINJAUAN

Berdasarkan analisis latar belakang, identifikasi masalah, dan tinjauan pustaka serta institusi, dapat disimpulkan bahwa:

1. Pusat Sembako memerlukan sistem informasi terintegrasi untuk mengelola operasional bisnis secara efisien
2. Teknologi web dengan arsitektur MVC menggunakan Flask dan SQLite merupakan solusi yang tepat
3. Implementasi database relasional yang terstruktur akan meningkatkan data integrity dan accessibility
4. Fitur-fitur seperti real-time tracking, automated payment verification, dan member rewards akan memberikan value tambahan
5. Deployment ke Hugging Face Spaces akan memastikan aplikasi dapat diakses 24/7 dengan minimal maintenance

---

**Catatan**: Dokumen ini dapat disesuaikan dengan data actual dari institusi Pusat Sembako dan requirements spesifik yang mungkin berbeda.
