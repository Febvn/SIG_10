# 🚀 Deploy FULL STACK di Render (Paling Mudah!)

## 🎯 Kenapa Render?

✅ **Satu platform** untuk frontend, backend, dan database
✅ **Free tier** tersedia
✅ **PostgreSQL + PostGIS** built-in
✅ **Auto deploy** dari GitHub
✅ **SSL/HTTPS** otomatis
❌ Backend sleep setelah 15 menit tidak digunakan (free tier)

---

## 📋 Prerequisites

- GitHub account
- Render account (https://render.com)
- Repository sudah di GitHub

---

## STEP 1: Push ke GitHub

```bash
cd c:\Users\muham\Videos\PublicMap\SIG_10

git init
git add .
git commit -m "Initial commit - WebGIS Lampung"

# Create repo di GitHub, lalu:
git remote add origin https://github.com/username/webgis-lampung.git
git branch -M main
git push -u origin main
```

---

## STEP 2: Deploy Database di Render

1. **Login** ke https://dashboard.render.com
2. **New** → **PostgreSQL**
3. **Setup**:
   - Name: `webgis-lampung-db`
   - Database: `db_gis_itera`
   - User: `postgres`
   - Region: **Singapore** (terdekat ke Indonesia)
   - Plan: **Free**
4. **Create Database**
5. **Copy** Internal Database URL dari dashboard
6. **Connect** via psql shell (di dashboard):
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```

**Save** Internal Database URL:
```
postgresql://postgres:xxxxx@dpg-xxxxx.singapore-postgres.render.com/db_gis_itera
```

---

## STEP 3: Deploy Backend di Render

1. **New** → **Web Service**
2. **Connect** GitHub repository
3. **Configure**:
   - Name: `webgis-lampung-api`
   - Region: **Singapore**
   - Branch: `main`
   - Root Directory: `.` (kosong atau root)
   - Runtime: **Python 3**
   - Build Command:
     ```bash
     pip install -r requirements.txt
     ```
   - Start Command:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - Plan: **Free**

4. **Environment Variables** (Advanced):
   ```
   DATABASE_URL=<paste Internal Database URL dari Step 2>
   PYTHON_VERSION=3.11.6
   ```

5. **Create Web Service**

6. **Tunggu deploy** (5-10 menit pertama kali)

7. **Setelah deploy sukses**, buka **Shell** tab di dashboard:
   ```bash
   python seed_real_data_bandarlampung.py
   python seed_lampung_province.py
   ```

**Save** Backend URL:
```
https://webgis-lampung-api.onrender.com
```

---

## STEP 4: Update Frontend untuk Production

**File**: `frontend/src/constants.js`

```javascript
// Update BASE_URL dengan backend Render
export const BASE_URL = import.meta.env.VITE_API_URL || 'https://webgis-lampung-api.onrender.com';
export const API_URL = `${BASE_URL}/geojson`;
export const MAP_CENTER = [-5.3971, 105.2677];

export const CATEGORIES = {
  'Masjid': { color: '#3b82f6' },
  'Sekolah': { color: '#ef4444' },
  'Puskesmas': { color: '#10b981' },
  'Minimarket': { color: '#f59e0b' },
  'Taman': { color: '#84cc16' },
  'Default': { color: '#6b7280' }
};
```

**Commit**:
```bash
git add frontend/src/constants.js
git commit -m "Update API URL for Render production"
git push
```

---

## STEP 5: Update CORS di Backend

**File**: `main.py`

Cari bagian CORS dan update:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://webgis-lampung.onrender.com",  # Nanti setelah deploy frontend
        "*"  # Sementara allow all (untuk testing)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Commit**:
```bash
git add main.py
git commit -m "Update CORS for Render"
git push
```

Render akan auto-redeploy backend!

---

## STEP 6: Deploy Frontend di Render

1. **New** → **Static Site**
2. **Connect** same GitHub repository
3. **Configure**:
   - Name: `webgis-lampung`
   - Region: **Singapore**
   - Branch: `main`
   - Root Directory: `frontend`
   - Build Command:
     ```bash
     npm install && npm run build
     ```
   - Publish Directory: `dist`
   - Plan: **Free**

4. **Environment Variables**:
   ```
   VITE_API_URL=https://webgis-lampung-api.onrender.com
   ```

5. **Create Static Site**

6. **Tunggu deploy** (3-5 menit)

**Frontend URL**:
```
https://webgis-lampung.onrender.com
```

---

## STEP 7: Final CORS Update

Sekarang update CORS dengan URL frontend yang benar:

**File**: `main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://webgis-lampung.onrender.com"  # URL frontend Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Commit & push**:
```bash
git add main.py
git commit -m "Final CORS config"
git push
```

---

## ✅ DONE! Your App is LIVE!

🌐 **Frontend**: https://webgis-lampung.onrender.com
🔌 **Backend API**: https://webgis-lampung-api.onrender.com
📚 **API Docs**: https://webgis-lampung-api.onrender.com/docs
🗄️ **Database**: PostgreSQL internal di Render

---

## ⚠️ IMPORTANT - Free Tier Limitations

### Backend (Web Service)
- ⏰ **Sleep after 15 minutes** inactivity
- ⚡ First request setelah sleep: **30-60 detik** cold start
- 💾 Disk storage: Tidak persistent
- 🌍 Uptime: Tidak 24/7

### Database (PostgreSQL)
- 💾 Storage: **1GB**
- 🔗 Connections: **97 concurrent**
- 🗓️ Retention: **90 hari** (expired setelah 90 hari tidak digunakan)

### Frontend (Static Site)
- ✅ **No limitations** significant
- 🚀 CDN global
- ⚡ Fast loading

### Solutions untuk Limitations:

**Opsi 1: UptimeRobot (FREE)**
- Keep backend awake dengan ping setiap 5 menit
- Sign up: https://uptimerobot.com
- Add monitor: https://webgis-lampung-api.onrender.com/

**Opsi 2: Upgrade ke Paid**
- Backend: $7/month (no sleep, persistent storage)
- Database: $7/month (no expiry)

---

## 🔧 Troubleshooting

### "Application failed to respond"
- Backend sedang cold start (tunggu 30-60 detik)
- Atau backend error (cek Logs di dashboard)

### Database connection error
- Check DATABASE_URL di environment variables
- Pastikan PostGIS extension installed

### Frontend tidak load data
- Check Network tab di browser console
- Pastikan backend URL benar di constants.js
- Pastikan CORS configured

### Detection upload gagal
- File terlalu besar (max 100MB free tier)
- Upload timeout (cold start backend)

---

## 📊 Alternative: Jika Backend Sering Sleep

Deploy backend di tempat lain yang tidak sleep:

### Railway (500 jam/bulan - ~20 hari)
- Frontend: Render
- Backend + DB: Railway
- FREE tier lebih generous

### PythonAnywhere (No sleep!)
- Frontend: Render atau Vercel
- Backend: PythonAnywhere (always on)
- DB: Supabase atau ElephantSQL

---

## 💰 Total Cost

| Component | Free Tier | Paid Tier |
|-----------|-----------|-----------|
| Frontend | ✅ FREE | $7/mo |
| Backend | ✅ FREE (with sleep) | $7/mo |
| Database | ✅ FREE (90d limit) | $7/mo |
| **TOTAL** | **$0/mo** | **$21/mo** |

---

## 🚀 Next Steps

1. ✅ Setup custom domain
2. ✅ Add monitoring (UptimeRobot)
3. ✅ Setup analytics
4. ✅ Enable automated backups (database)
5. ✅ Add error logging (Sentry)

**Selamat! Aplikasi Anda sudah ONLINE dan bisa diakses dari mana saja!** 🎉

---

## 📝 Quick Links

- **Render Dashboard**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **UptimeRobot**: https://uptimerobot.com
- **GitHub Repo**: https://github.com/username/webgis-lampung
