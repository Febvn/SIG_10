# 🚂 Deploy ke Railway - Panduan Lengkap

## Persiapan

### 1. Install Railway CLI (Opsional)
```bash
npm install -g @railway/cli
```

### 2. File yang Sudah Disiapkan
- ✅ `nixpacks.toml` - Konfigurasi build Railway
- ✅ `requirements.txt` - Sudah menggunakan `opencv-python-headless`
- ✅ `Dockerfile` - Backup jika ingin gunakan Docker

## Cara Deploy

### Opsi A: Deploy via Dashboard Railway (Paling Mudah)

#### Step 1: Buat Project Baru
1. Login ke [railway.app](https://railway.app)
2. Klik **"New Project"**
3. Pilih **"Deploy from GitHub repo"**
4. Pilih repository Anda

#### Step 2: Tambahkan Database PostgreSQL
1. Di dashboard project, klik **"+ New"**
2. Pilih **"Database"** → **"Add PostgreSQL"**
3. Railway akan otomatis membuat database

#### Step 3: Setup Environment Variables
Klik service backend Anda, pilih tab **"Variables"**, tambahkan:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your-super-secret-key-min-32-karakter
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Tips:** Railway otomatis mengenali `${{Postgres.DATABASE_URL}}`

#### Step 4: Deploy
1. Railway akan otomatis build dan deploy
2. Tunggu sampai status berubah jadi **"Active"** atau **"Running"**
3. Klik service → **"Settings"** → **"Generate Domain"** untuk mendapatkan URL public

### Opsi B: Deploy via Railway CLI

```bash
# Login
railway login

# Link ke project atau buat baru
railway init

# Tambahkan PostgreSQL
railway add

# Set environment variables
railway variables set SECRET_KEY="your-secret-key-here"

# Deploy
railway up

# Buka di browser
railway open
```

## Environment Variables yang Diperlukan

| Variable | Nilai | Keterangan |
|----------|-------|------------|
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Otomatis dari Railway Postgres |
| `SECRET_KEY` | String acak 32+ karakter | Untuk JWT token |
| `ALGORITHM` | `HS256` | Algoritma JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Durasi token |

## Troubleshooting

### ❌ Error: "libxcb.so.1: cannot open shared object file"

**Penyebab:** Library sistem untuk OpenCV tidak tersedia

**Solusi:**
1. ✅ Pastikan `nixpacks.toml` ada di root project
2. ✅ Pastikan menggunakan `opencv-python-headless` di `requirements.txt`
3. Redeploy project

### ❌ Error: "Application failed to respond"

**Penyebab:** Port tidak match dengan Railway

**Solusi:** Pastikan di `nixpacks.toml` atau Dockerfile menggunakan `$PORT`:
```toml
[start]
cmd = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### ❌ Error: "Connection to database failed"

**Penyebab:** Database belum dibuat atau `DATABASE_URL` salah

**Solusi:**
1. Pastikan PostgreSQL service sudah dibuat
2. Gunakan `${{Postgres.DATABASE_URL}}` (dengan kurung kurawal ganda)
3. Restart service backend

### ❌ Build Failed dengan Python Version

**Solusi:** Buat file `runtime.txt`:
```
python-3.11.0
```

## Monitoring dan Logs

### Lihat Logs
```bash
# Via CLI
railway logs

# Via Dashboard
Project → Service → Logs tab
```

### Health Check
Setelah deploy, test endpoint:
```bash
curl https://your-app.railway.app/health
```

## Database Migration

Railway tidak menjalankan migration otomatis. Ada 2 cara:

### Cara 1: Manual via Railway CLI
```bash
railway run python create_database.py
```

### Cara 2: Tambahkan di Start Command
Edit `nixpacks.toml`:
```toml
[start]
cmd = "python create_database.py && uvicorn main:app --host 0.0.0.0 --port $PORT"
```

⚠️ **Warning:** Cara 2 akan run migration setiap kali deploy!

## Update Deployment

### Push ke GitHub
Railway otomatis redeploy setiap kali ada push ke branch utama:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Redeploy
Di Dashboard: Service → Deployments → Klik **"Redeploy"**

## Cost Estimation

Railway menawarkan:
- **Free Trial:** $5 kredit gratis
- **Hobby Plan:** $5/bulan
- **Usage-based:** Bayar sesuai penggunaan

Estimasi project ini: ~$2-3/bulan untuk backend + database kecil

## Scaling

Railway otomatis scale berdasarkan traffic, tapi untuk optimize:

1. **Horizontal Scaling:** Railway Pro plan
2. **Optimize Memory:** 
   - Gunakan `opencv-python-headless` (sudah dilakukan ✅)
   - Hindari load model besar ke memory

## Next Steps

- [ ] Setup custom domain di Settings
- [ ] Enable auto-deploy dari GitHub
- [ ] Setup monitoring dengan Railway metrics
- [ ] Backup database secara berkala

## Useful Links

- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Nixpacks Docs](https://nixpacks.com/docs)

---

## Quick Command Reference

```bash
# Status
railway status

# Logs (follow)
railway logs -f

# Run command di Railway
railway run <command>

# Connect ke database
railway connect

# List services
railway service

# Open in browser
railway open
```
