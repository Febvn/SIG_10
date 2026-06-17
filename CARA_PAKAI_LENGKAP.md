# 🗺️ CARA PAKAI WEBGIS BANDAR LAMPUNG - LENGKAP

## 📊 DATA YANG TERSEDIA

Database sudah terisi dengan **75 FASILITAS REAL** di Bandar Lampung:

- ✅ **MASJID**: 15 (Masjid Agung Al-Furqon, dll)
- ✅ **SEKOLAH**: 20 (SMAN 1, Unila, ITERA, dll)
- ✅ **PUSKESMAS**: 12 (Puskesmas Kedaton, dll)
- ✅ **MINIMARKET**: 18 (Indomaret, Alfamart, dll)
- ✅ **TAMAN**: 10 (Taman Gajah, Tahura, dll)

Semua dengan **koordinat GPS ASLI** dan **alamat lengkap**!

---

## 🚀 CARA PAKAI

### 1️⃣ Buka Aplikasi

**Frontend**: http://localhost:5173/
**Backend**: http://127.0.0.1:8000

### 2️⃣ Mode Awal (Peta Kosong)

Saat pertama buka, peta akan **KOSONG** dan stats menunjukkan **0**:
```
0  TOTAL
0  MASJID
0  SEKOLAH
0  PUSKESMAS
0  MINIMARKET
0  TAMAN
```

### 3️⃣ Aktifkan Mode "Area"

1. Klik tombol **"Area"** di sidebar (tombol pertama)
2. UI akan berubah menampilkan:
   - 📍 Icon dengan text "Klik di Peta"
   - Slider radius (100m - 5000m)
   - Instruksi: "Tap anywhere on the map..."

### 4️⃣ Klik di Peta

**Pilih lokasi yang ingin dieksplorasi:**

#### 📍 Area Rekomendasi:

**A. Tanjung Karang (Pusat Kota)**
- Koordinat: -5.4292, 105.2622
- Banyak: Sekolah, Masjid, Taman
- Radius 2km → ~20 fasilitas

**B. Way Halim**
- Koordinat: -5.3971, 105.2677
- Banyak: Masjid, Minimarket
- Radius 2km → ~15 fasilitas

**C. Sukarame**
- Koordinat: -5.3755, 105.2890
- Banyak: Minimarket, Sekolah
- Radius 2km → ~12 fasilitas

**D. Rajabasa**
- Koordinat: -5.3845, 105.2801
- Banyak: Puskesmas, Sekolah, Minimarket
- Radius 2km → ~18 fasilitas

### 5️⃣ Lihat Hasilnya! 🎉

Setelah klik di peta, otomatis akan muncul:

#### Di Sidebar:
```
20 TOTAL
5  MASJID
6  SEKOLAH
1  PUSKESMAS
4  MINIMARKET
4  TAMAN
```

#### Di Peta:
- ✅ **Circle hijau** menunjukkan area radius
- ✅ **Marker hijau pulse** di titik yang diklik
- ✅ **Marker warna-warni** untuk setiap fasilitas:
  - 🕌 **Biru**: Masjid
  - 🏫 **Merah**: Sekolah
  - 🏥 **Hijau**: Puskesmas
  - 🏪 **Oranye**: Minimarket
  - 🌳 **Hijau muda**: Taman

#### Di List Fasilitas:
```
📋 EXPLORE NEARBY - 20 items

🏫 SMAN 1 Bandar Lampung
   Jl. Kartini No. 2                    0m

🌳 Taman Kartini
   Jl. Kartini                         67m

🕌 Masjid Al-Ikhlas
   Jl. Kartini                         79m
   
...dst
```

### 6️⃣ Interaksi Lanjutan

#### A. Klik Marker di Peta
- Popup akan muncul dengan detail fasilitas
- Info: Nama, Jenis, Alamat
- Tombol: Edit, Delete (jika sudah login)

#### B. Klik Item di List
- Peta akan zoom ke lokasi tersebut
- Item akan highlight

#### C. Filter by Category
- Klik widget kategori (MASJID, SEKOLAH, dll)
- Hanya marker kategori itu yang ditampilkan
- Markers akan **pulse** (animasi)

#### D. Search
- Ketik di search bar
- Filter by nama atau jenis
- Real-time filtering

#### E. Ubah Radius
- Geser slider radius (100m - 5000m)
- Klik "Clear & Search New Area"
- Klik lagi di peta untuk search ulang dengan radius baru

---

## 🎯 FITUR DETECTION

### Upload & Detect Objects

1. **Klik tombol "Detect"** (tombol ketiga)
2. **Upload file**: TIF/JPG/PNG wilayah Bandar Lampung
3. **Tunggu proses** (10-60 detik)
4. **Lihat hasil**:
   - Bounding box **MERAH** di objek terdeteksi
   - Label: "🎯 [NAMA_OBJEK]"
   - Popup dengan confidence %

### Sample Files untuk Test:
```
data/tif_samples/lampung2_unila.tif
data/tif_samples/lampung3_tanjungkarang.tif
data/tif_samples/lampung4_bakauheni.tif
```

---

## 🔐 FITUR CRUD (Create, Update, Delete)

### Login Dulu
1. Klik "Login" atau "Sign Up"
2. Register user baru atau login

### Tambah Fasilitas
1. **Klik "Tambah"** (tombol kedua)
2. **Klik di peta** untuk set lokasi
3. **Isi form**:
   - Nama (min 3 karakter)
   - Jenis (pilih kategori)
   - Alamat (min 5 karakter)
4. **Klik "Create"**

### Edit Fasilitas
1. **Klik marker** di peta
2. **Klik "Edit"** di popup
3. **Ubah data**
4. **Klik "Update"**

### Hapus Fasilitas
1. **Klik marker** di peta
2. **Klik "Delete"** di popup
3. **Confirm**

---

## 🎨 BASEMAP OPTIONS

Klik control di kanan bawah peta:
- 🌙 **Dark**: Peta gelap (default)
- 🗺️ **Street**: Peta jalan
- 🛰️ **Satellite**: Citra satelit

---

## 📊 TEST DENGAN SCRIPT

### Test Nearby API:
```bash
python test_nearby_api.py
```

### Test Detection:
```bash
python test_detection_api.py
```

---

## 🐛 TROUBLESHOOTING

### Stats tetap 0?
- Pastikan mode "Area" aktif
- Klik di peta Bandar Lampung
- Cek radius tidak terlalu kecil

### Marker tidak muncul?
- Refresh browser (Ctrl+F5)
- Cek console browser untuk error
- Pastikan backend running

### Backend error?
- Cek PostgreSQL running
- Cek database `db_gis_itera` ada
- Run: `python seed_real_data_bandarlampung.py`

---

## 📝 SUMMARY WORKFLOW

```
1. Buka http://localhost:5173
2. Klik "Area"
3. Klik di peta Bandar Lampung
4. Lihat stats update + markers muncul
5. Eksplorasi:
   - Klik marker untuk detail
   - Klik kategori untuk filter
   - Ubah radius dan search ulang
6. (Opsional) Upload TIF untuk detection
7. (Opsional) Login untuk CRUD
```

---

## 🎉 SELAMAT MENCOBA!

Database sudah berisi **75 fasilitas REAL** di Bandar Lampung.
Semua koordinat sudah **AKURAT** dan bisa langsung digunakan!

**Happy Mapping!** 🗺️✨
