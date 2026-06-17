# 🚀 Deploy ke Railway + Vercel (GRATIS!)

## 📋 Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)

---

## STEP 1: Push ke GitHub

```bash
cd c:\Users\muham\Videos\PublicMap\SIG_10

# Initialize git (jika belum)
git init
git add .
git commit -m "Initial commit - WebGIS Lampung"

# Create repo di GitHub, lalu:
git remote add origin https://github.com/username/webgis-lampung.git
git branch -M main
git push -u origin main
```

---

## STEP 2: Deploy Database di Railway

1. **Buka**: https://railway.app
2. **Login** dengan GitHub
3. **New Project** → **Provision PostgreSQL**
4. **Copy** `DATABASE_URL` dari Variables tab
5. **Connect to Database** via Railway CLI atau web console:
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```

---

## STEP 3: Deploy Backend di Railway

1. **New Service** di project yang sama
2. **Deploy from GitHub repo**
3. **Select repository**: webgis-lampung
4. **Settings** → **Environment**:
   - Root Directory: `/`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Variables** → Add:
   ```
   DATABASE_URL=<paste dari PostgreSQL service>
   PORT=8000
   ```
6. **Deploy**!

7. **Setelah deploy sukses**, jalankan seed via Railway console:
   ```bash
   python seed_real_data_bandarlampung.py
   python seed_lampung_province.py
   ```

8. **Copy** URL backend: `https://xxx.railway.app`

---

## STEP 4: Update Frontend Config

**File**: `frontend/src/constants.js`

```javascript
export const BASE_URL = import.meta.env.VITE_API_URL || 'https://your-railway-backend.railway.app';
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

**Commit & push**:
```bash
git add .
git commit -m "Update API URL for production"
git push
```

---

## STEP 5: Deploy Frontend di Vercel

1. **Buka**: https://vercel.com
2. **Import Project** → **From GitHub**
3. **Select** webgis-lampung repo
4. **Configure**:
   - Framework Preset: **Vite**
   - Root Directory: **frontend**
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Environment Variables**:
   ```
   VITE_API_URL=https://your-railway-backend.railway.app
   ```
6. **Deploy**!

---

## STEP 6: Update CORS di Backend

**File**: `main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-vercel-app.vercel.app"  # Tambahkan domain Vercel Anda
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Commit & push**:
```bash
git add main.py
git commit -m "Update CORS for production"
git push
```

Railway akan auto-redeploy!

---

## ✅ DONE!

Your app is now live at:
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-backend.railway.app
- **API Docs**: https://your-backend.railway.app/docs

---

## 🔧 Troubleshooting

### Database Connection Error
- Check DATABASE_URL di Railway variables
- Pastikan PostGIS extension installed

### CORS Error
- Update `allow_origins` di main.py
- Redeploy backend

### Frontend API Error
- Check VITE_API_URL di Vercel
- Pastikan tanpa trailing slash

### Railway App Sleep
- Free tier: 500 jam/bulan
- Upgrade ke Pro ($5/mo) untuk unlimited

---

## 💰 BIAYA

- **Railway Database**: FREE (512MB storage)
- **Railway Backend**: FREE (500 jam/bulan)
- **Vercel Frontend**: FREE (unlimited bandwidth)
- **Total**: **$0/bulan** ✅

---

## 🚀 Next Steps

1. Custom domain (opsional)
2. Setup monitoring
3. Enable analytics
4. Add CI/CD pipeline

**Selamat! Aplikasi Anda sudah online!** 🎉
