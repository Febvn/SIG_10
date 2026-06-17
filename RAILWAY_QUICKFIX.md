# 🚨 Railway Crash - Quick Fix

## Problem
```
ImportError: libxcb.so.1: cannot open shared object file: No such file or directory
```

## ✅ Solusi Sudah Diterapkan

File yang sudah diupdate:

1. **`nixpacks.toml`** ✅ - Menambahkan library sistem yang dibutuhkan OpenCV
2. **`requirements.txt`** ✅ - Ganti `opencv-python` → `opencv-python-headless`
3. **`runtime.txt`** ✅ - Pin Python version ke 3.11.0
4. **`Dockerfile`** ✅ - Tambahkan library X11 (untuk backup)

## 🚀 Steps untuk Deploy Ulang

### 1. Commit & Push Changes
```bash
git add .
git commit -m "Fix: Add Railway deployment config and OpenCV dependencies"
git push origin main
```

### 2. Railway akan Otomatis Redeploy
- Tunggu 2-5 menit
- Cek status di Railway Dashboard

### 3. Kalau Masih Error, Manual Redeploy
Di Railway Dashboard:
1. Pilih service yang crash
2. Klik tab **"Deployments"**
3. Klik **"Redeploy"** pada deployment terbaru

## 📋 Checklist Setelah Deploy Sukses

- [ ] Service status = **"Active"** atau **"Running"**
- [ ] Generate public domain di Settings
- [ ] Test endpoint: `https://your-app.railway.app/health`
- [ ] Setup environment variables (lihat DEPLOY_RAILWAY.md)
- [ ] Tambahkan PostgreSQL database
- [ ] Run database migration

## 🔍 Debugging

### Lihat Logs Real-time
```bash
railway logs -f
```

Atau di Dashboard: Service → Logs tab

### Test Local dengan Headless OpenCV
```bash
pip install opencv-python-headless==4.8.1.78
python -c "import cv2; print(cv2.__version__)"
```

### Cek Nixpacks Build
Railway menggunakan Nixpacks, pastikan:
- `nixpacks.toml` ada di root folder ✅
- File tidak ada typo ✅

## Environment Variables yang Harus Diset

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Kenapa Pakai opencv-python-headless?

| Package | Ukuran | GUI Support | Cocok untuk |
|---------|--------|-------------|-------------|
| `opencv-python` | ~90MB | ✅ Ya | Desktop apps |
| `opencv-python-headless` | ~30MB | ❌ Tidak | **Servers/Cloud** ✅ |

Railway adalah server (headless), jadi kita pakai versi headless yang lebih ringan dan tidak butuh X11 library.

## Next Steps

Kalau deploy berhasil, lanjut ke:
1. Test semua endpoint (auth, fasilitas, detection)
2. Upload sample TIF file
3. Setup frontend untuk connect ke Railway URL

---

**Note:** Perubahan ini juga membuat Dockerfile lebih baik untuk deployment di Render atau platform lain! 🎉
