# 🧹 Railway: Clear Cache & Force Rebuild

## Masalah
Railway masih menggunakan **cache lama** yang berisi `opencv-python` (bukan headless), sehingga error `libxcb.so.1` masih terjadi meskipun `requirements.txt` sudah diupdate.

## ✅ Solusi: Clear Build Cache

### Opsi 1: Via Railway Dashboard (Recommended)

1. **Buka Railway Dashboard**
   - Login ke [railway.app](https://railway.app)
   - Pilih project Anda
   - Klik service backend yang crash

2. **Clear Cache & Redeploy**
   - Klik tab **"Settings"** (⚙️)
   - Scroll ke bawah sampai **"Danger Zone"**
   - Klik **"Clear Build Cache"**
   - Konfirmasi

3. **Trigger Redeploy**
   - Kembali ke tab **"Deployments"**
   - Klik tombol **"Redeploy"** pada deployment terakhir
   - Atau klik **"Deploy"** → **"Deploy Latest Commit"**

### Opsi 2: Via Railway CLI

```bash
# Login
railway login

# Link ke project
railway link

# Trigger redeploy (akan clear cache otomatis jika ada perubahan)
railway up --detach
```

### Opsi 3: Force Rebuild dengan Empty Commit

```bash
# Buat empty commit untuk trigger rebuild
git commit --allow-empty -m "Force Railway rebuild - clear cache"
git push origin main
```

## 🔍 Verifikasi Setelah Deploy

### 1. Cek Logs Build
Di Railway Dashboard → Deployments → Klik deployment terbaru → Tab **"Build Logs"**

**Yang harus dicari:**
```
✓ Installing python packages
  ✓ pip install --no-cache-dir -r requirements.txt
  ✓ Successfully installed opencv-python-headless-4.8.1.78
```

**BUKAN:**
```
✗ Successfully installed opencv-python-4.8.1.78  ← INI SALAH!
```

### 2. Cek Deploy Logs
Tab **"Deploy Logs"** - pastikan tidak ada error:
```
✓ Application started successfully
✓ Uvicorn running on 0.0.0.0:$PORT
```

### 3. Test Health Endpoint
Setelah deploy sukses, test:
```bash
curl https://your-app.railway.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "python_version": "3.11.x",
  "opencv": "cv2 4.8.1 - /app/.venv/lib/python3.11/site-packages/cv2"
}
```

## 🚨 Jika Masih Error

### Debug Step-by-Step:

1. **Cek Python Version di Build Logs**
   ```
   Should be: Python 3.11.x ✅
   NOT: Python 3.13.x ❌
   ```

2. **Cek Package yang Terinstall**
   Di Build Logs, cari:
   ```
   opencv-python-headless==4.8.1.78 ✅
   ```
   
   Bukan:
   ```
   opencv-python==4.8.1.78 ❌
   ```

3. **Cek System Packages**
   Di Build Logs, pastikan ada:
   ```
   Installing apt packages: libgl1-mesa-glx, libglib2.0-0, libsm6, 
   libxext6, libxrender1, libgomp1, libxcb1, gdal-bin, libgdal-dev
   ```

4. **Restart Service**
   - Settings → **"Restart Service"**

5. **Delete & Recreate Service (Last Resort)**
   - Hapus service lama di Railway
   - Buat service baru dari GitHub repo yang sama

## 📋 Checklist

- [ ] `requirements.txt` berisi `opencv-python-headless` (bukan `opencv-python`)
- [ ] `nixpacks.toml` ada di root folder
- [ ] `runtime.txt` berisi `python-3.11.0`
- [ ] `.railwayignore` ada (opsional tapi membantu)
- [ ] Push semua perubahan ke Git
- [ ] Clear build cache di Railway
- [ ] Redeploy dari dashboard
- [ ] Cek build logs untuk verify packages
- [ ] Test `/health` endpoint

## 🎯 Expected Build Output

```bash
# Build Logs
══════════════════════════════════════════
📦 Installing dependencies
══════════════════════════════════════════
✓ Installing apt packages
  ✓ libgl1-mesa-glx
  ✓ libglib2.0-0
  ✓ libxcb1
  ✓ gdal-bin
  ✓ libgdal-dev

✓ Installing python packages
  ✓ pip install --no-cache-dir -r requirements.txt
  ✓ opencv-python-headless-4.8.1.78
  ✓ rasterio-1.3.9
  ✓ ultralytics-8.0.227

══════════════════════════════════════════
🚀 Starting application
══════════════════════════════════════════
✓ uvicorn main:app --host 0.0.0.0 --port $PORT
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 💡 Tips

1. **Selalu clear cache** jika ganti package major (opencv-python → opencv-python-headless)
2. **Tunggu 3-5 menit** untuk build selesai sepenuhnya
3. **Gunakan `/health` endpoint** untuk debug info
4. **Check environment variables** - pastikan `DATABASE_URL` dan `SECRET_KEY` sudah diset

## 🔗 Links

- [Railway Docs - Build Cache](https://docs.railway.app/reference/builds#cache)
- [Nixpacks Docs](https://nixpacks.com/docs)
- [Railway Discord](https://discord.gg/railway) - untuk bantuan

---

**Last Updated:** $(Get-Date -Format "yyyy-MM-dd HH:mm")
