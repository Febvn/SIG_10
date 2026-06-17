# 🐳 Railway: Switch to Dockerfile

Jika Nixpacks masih bermasalah, gunakan Dockerfile yang lebih reliable.

## ⚙️ Steps to Switch

### 1. Update Railway Settings

**Via Dashboard:**

1. Login ke [railway.app](https://railway.app)
2. Pilih project → Klik service backend
3. Klik tab **"Settings"**
4. Scroll ke section **"Build"**
5. Ubah **"Builder"** dari "Nixpacks" ke **"Dockerfile"**
6. Scroll ke bawah, klik **"Save Changes"**

### 2. Trigger Redeploy

Setelah ganti builder:

1. Kembali ke tab **"Deployments"**
2. Klik **"Redeploy"** atau **"New Deployment"**
3. Railway akan build menggunakan `Dockerfile`

### 3. Monitor Build

**Build Logs akan menampilkan:**

```dockerfile
#1 [internal] load build definition from Dockerfile
#2 [internal] load metadata for docker.io/library/python:3.11-slim
#3 [1/6] FROM docker.io/library/python:3.11-slim
#4 [2/6] WORKDIR /app
#5 [3/6] RUN apt-get update && apt-get install -y --no-install-recommends...
  ✓ libpq-dev
  ✓ gdal-bin
  ✓ libgl1-mesa-glx
  ✓ libglib2.0-0
#6 [4/6] COPY requirements.txt .
#7 [5/6] RUN pip install --no-cache-dir -r requirements.txt
  ✓ opencv-python-headless==4.8.1.78
  ✓ ultralytics==8.0.227
  ✓ rasterio==1.3.9
#8 [6/6] COPY . .
#9 exporting to image
✓ Build complete!
```

## ✅ Advantages of Using Dockerfile

| Feature | Nixpacks | Dockerfile |
|---------|----------|------------|
| **Kontrol penuh** | ❌ Terbatas | ✅ Full control |
| **Cache predictable** | ⚠️ Kadang bermasalah | ✅ Reliable |
| **System packages** | ⚠️ Via nixpacks.toml | ✅ Langsung di RUN |
| **Debugging** | ❌ Sulit | ✅ Mudah |
| **Portability** | ❌ Hanya Railway/Nixpacks | ✅ Docker universal |

## 🔍 Verify Dockerfile Locally (Optional)

Test di komputer Anda sebelum deploy:

```bash
# Build image
docker build -t sig10-backend .

# Run container
docker run -p 8000:8000 -e DATABASE_URL="your-db-url" sig10-backend

# Test
curl http://localhost:8000/health
```

## 📋 Environment Variables

Pastikan sudah set di Railway:

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your-secret-key-32-chars-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=8000  # Railway set otomatis
```

## 🚨 Troubleshooting

### Error: "Dockerfile not found"

**Solution:** Pastikan `Dockerfile` (huruf besar D) ada di root project.

```bash
# Check
ls -la | grep Dockerfile
```

### Error: "Context deadline exceeded"

**Solution:** Build timeout - image terlalu besar.

1. Pastikan `.dockerignore` sudah dibuat
2. Exclude folder besar (assets, .git, dll)

### Error: "Port already in use"

**Solution:** Railway menggunakan environment variable `$PORT`.

Dockerfile sudah benar menggunakan:
```dockerfile
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Build sangat lambat

**Solution:** Optimize Dockerfile layers.

Sudah dioptimize di Dockerfile terbaru:
- `--no-install-recommends` untuk apt
- `--no-cache-dir` untuk pip
- `rm -rf /var/lib/apt/lists/*` untuk cleanup

## 💡 Tips

1. **Dockerfile lebih reliable** daripada Nixpacks untuk project Python complex
2. **Cache Docker layers** - urutan COPY penting:
   - Copy `requirements.txt` dulu
   - Install dependencies
   - Copy source code terakhir
3. **Use slim base image** - `python:3.11-slim` lebih kecil dari `python:3.11`

## 🔄 Switch Back to Nixpacks (If Needed)

Jika mau balik ke Nixpacks:

1. Settings → Build section
2. Ubah "Dockerfile" ke "Nixpacks"
3. Redeploy

---

## Quick Checklist

- [ ] Dockerfile sudah ada di root project
- [ ] .dockerignore sudah dibuat
- [ ] requirements.txt berisi opencv-python-headless
- [ ] Railway builder diubah ke "Dockerfile"
- [ ] Environment variables sudah diset
- [ ] Redeploy triggered
- [ ] Build logs tidak ada error
- [ ] Test /health endpoint

**Dockerfile approach adalah solusi paling reliable! 🐳**
