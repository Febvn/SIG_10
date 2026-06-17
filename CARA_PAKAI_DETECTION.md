# 🎯 CARA PAKAI OBJECT DETECTION

## Step-by-Step Simple Guide

### 1. Pastikan Server Running ✅
```bash
# Backend harus running di http://127.0.0.1:8000
# Frontend harus running di http://localhost:5173
```

### 2. Buka Aplikasi 🌐
- Buka browser
- Akses: **http://localhost:5173/**

### 3. Klik Tombol "Detect" 🔍
- Di sidebar kiri, ada 3 tombol: **Area**, **Tambah**, **Detect**
- Klik tombol **"Detect"** (paling kanan)
- Form upload akan muncul

### 4. Upload Gambar 📤
- Klik tombol **"Upload & Detect"**
- Pilih file gambar:
  - **TIF** (paling bagus, ada koordinat GPS) ✅
  - **JPG** (bisa, tapi tanpa GPS)
  - **PNG** (bisa, tapi tanpa GPS)

### 5. Tunggu Proses ⏳
- Loading akan muncul
- Tunggu 10-60 detik (tergantung ukuran gambar)
- Notifikasi akan muncul saat selesai

### 6. Lihat Hasil 🎉
Yang akan muncul:

#### Di Peta:
- ✅ Peta otomatis zoom ke wilayah yang di-upload
- ✅ **Bounding box MERAH** muncul di objek yang terdeteksi
- ✅ **Label nama objek** muncul dengan icon 🎯
- ✅ Label akan **beranimasi pulse** (naik-turun)

#### Di Sidebar:
- ✅ Jumlah objek terdeteksi
- ✅ List class objek yang ditemukan

### 7. Klik Bounding Box untuk Detail 📊
- Klik kotak merah
- Popup akan muncul dengan:
  - 🎯 Icon
  - Nama objek (contoh: "roundabout", "building")
  - Confidence (tingkat keyakinan) dalam %

## 🧪 Test dengan Sample

Coba dengan sample file yang sudah ada:

### Lokasi Sample Files:
```
data/tif_samples/lampung2_unila.tif      <- Area ITERA
data/tif_samples/lampung3_tanjungkarang.tif
data/tif_samples/lampung4_bakauheni.tif
data/tif_samples/lampung5_natar.tif
data/tif_samples/lampung8_telukbetung.tif
```

### Hasil Yang Diharapkan:
- **lampung2_unila.tif** → Deteksi: Roundabout, Buildings
- Koordinat: Sekitar ITERA (105.24, -5.36)
- Peta akan zoom ke lokasi ITERA

## 🎨 Tampilan Visual

```
┌─────────────────────────────────────┐
│  PETA (Satellite View)              │
│                                     │
│     ┌──────────────┐                │
│     │  🎯 ROUNDABOUT│ ← Label       │
│     ├──────────────┤                │
│     │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← Box Merah    │
│     │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│   (Dashed)     │
│     └──────────────┘                │
│                                     │
└─────────────────────────────────────┘
```

## ⚙️ Settings (Opsional)

Jika ingin ubah sensitivity detection, edit di kode:
- File: `frontend/src/App.jsx`
- Line: `handleDetectObjects` function
- Parameter: `conf_threshold=0.25`
  - **0.1-0.2** = Lebih banyak deteksi (banyak false positive)
  - **0.25-0.3** = Balanced ✅ (recommended)
  - **0.4-0.5** = Lebih sedikit deteksi (lebih akurat)

## 🐛 Kalau Error:

### "Detection failed"
- Cek backend server masih running
- Cek file format benar (TIF/JPG/PNG)
- Cek ukuran file tidak terlalu besar

### Bounding box tidak muncul
- Refresh browser (Ctrl+F5)
- Clear detection dengan klik tombol "Clear"
- Upload ulang

### Tidak ada objek terdeteksi
- Normal! Berarti di gambar memang tidak ada objek yang dikenali
- Coba gambar lain
- Atau turunkan confidence threshold

## 🎯 Tips Terbaik:

1. **Gunakan file TIF** - Punya koordinat GPS, langsung tepat di peta
2. **Gambar satelit** - Hasil lebih bagus dari foto biasa
3. **Resolusi tinggi** - Makin jelas makin bagus
4. **Area Bandar Lampung** - Model trained untuk area ini

## ✅ Checklist:

- [ ] Backend running (port 8000)
- [ ] Frontend running (port 5173)
- [ ] Buka http://localhost:5173
- [ ] Klik tombol "Detect"
- [ ] Upload gambar TIF/JPG/PNG
- [ ] Tunggu loading selesai
- [ ] Lihat bounding box merah di peta
- [ ] Klik box untuk lihat detail

## 🎉 DONE!

Sekarang Anda bisa detect objek dari gambar satelit Bandar Lampung!
