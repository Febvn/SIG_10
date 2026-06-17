# 🚀 DEPLOYMENT GUIDE - WebGIS Bandar Lampung

## 📦 Stack Yang Perlu Di-Deploy

Aplikasi ini terdiri dari 3 komponen:

1. **Database**: PostgreSQL + PostGIS
2. **Backend**: FastAPI (Python)
3. **Frontend**: React + Vite

---

## 🎯 OPSI DEPLOYMENT

### 1️⃣ **VERCEL (Frontend) + RAILWAY (Backend + DB)** ⭐ RECOMMENDED

**Biaya**: FREE tier available
**Kemudahan**: ⭐⭐⭐⭐⭐ (Paling mudah)

#### A. Deploy Database di Railway

1. **Buat akun**: https://railway.app
2. **New Project** → **Provision PostgreSQL**
3. **Install PostGIS**:
   ```bash
   # Dari Railway console
   CREATE EXTENSION postgis;
   ```
4. **Copy DATABASE_URL** dari Railway dashboard

#### B. Deploy Backend di Railway

1. **New Service** → **GitHub Repo**
2. **Connect** repository ini
3. **Root Directory**: `/` (root project)
4. **Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Environment Variables**:
   ```
   DATABASE_URL=<Railway PostgreSQL URL>
   ```
6. **Run seed**:
   ```bash
   python seed_real_data_bandarlampung.py
   python seed_lampung_province.py
   ```

#### C. Deploy Frontend di Vercel

1. **Buat akun**: https://vercel.com
2. **Import GitHub Repository**
3. **Root Directory**: `frontend`
4. **Framework**: Vite
5. **Environment Variables**:
   ```
   VITE_API_URL=https://<railway-backend-url>
   ```
6. **Deploy**!

**Update `constants.js`**:
```javascript
export const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

### 2️⃣ **RENDER (All-in-One)** 

**Biaya**: FREE tier (dengan limit)
**Kemudahan**: ⭐⭐⭐⭐

#### Setup:

1. **Database**: Render PostgreSQL (Free)
2. **Backend**: Web Service (Free - sleeps after 15 min)
3. **Frontend**: Static Site (Free)

**Pros**: Satu platform, mudah manage
**Cons**: Backend sleep setelah 15 menit tidak digunakan

**Link**: https://render.com

---

### 3️⃣ **HEROKU**

**Biaya**: $5-7/month (no free tier anymore)
**Kemudahan**: ⭐⭐⭐⭐

#### Setup:

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create app-name
   heroku addons:create heroku-postgresql:mini
   git push heroku main
   ```

---

### 4️⃣ **DIGITAL OCEAN / AWS / GOOGLE CLOUD**

**Biaya**: $5-50/month
**Kemudahan**: ⭐⭐

**Recommended untuk**:
- Production dengan traffic tinggi
- Butuh kontrol penuh
- Data sensitive

#### Setup Digital Ocean Droplet:

1. **Create Droplet**: Ubuntu 22.04
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip postgresql postgis nginx
   ```
3. **Setup PostgreSQL + PostGIS**
4. **Clone repo & install**
5. **Setup Nginx reverse proxy**
6. **Setup SSL dengan Certbot**

---

### 5️⃣ **DOCKER + ANY CLOUD**

**Biaya**: Tergantung provider
**Kemudahan**: ⭐⭐⭐

Saya bisa buatkan `Dockerfile` dan `docker-compose.yml`!

---

## 🎯 REKOMENDASI BERDASARKAN KEBUTUHAN

### 🆓 FREE / Belajar / Portfolio
→ **VERCEL + RAILWAY**
- Frontend: Vercel (unlimited bandwidth)
- Backend + DB: Railway (500 jam/bulan free)

### 💼 Production / Skripsi
→ **RENDER** atau **DIGITAL OCEAN**
- Lebih reliable
- No sleep
- Better performance

### 🏢 Enterprise / Commercial
→ **AWS / GOOGLE CLOUD / AZURE**
- Scalable
- Enterprise support
- Advanced features

---

## 📝 PERSIAPAN DEPLOYMENT

### 1. Update Frontend Constants

**File**: `frontend/src/constants.js`
```javascript
export const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_URL = `${BASE_URL}/geojson`;
```

### 2. Add CORS untuk Backend

**File**: `main.py`
```python
# Update origins dengan domain production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-vercel-domain.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Production Environment Variables

Create `.env.production`:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
PORT=8000
ENVIRONMENT=production
```

### 4. Build Frontend

```bash
cd frontend
npm run build
# Output di folder 'dist'
```

---

## 🔒 SECURITY CHECKLIST

- [ ] Ganti password database default
- [ ] Setup HTTPS/SSL
- [ ] Environment variables di .env (jangan commit!)
- [ ] Enable CORS hanya untuk domain production
- [ ] Rate limiting di backend
- [ ] Backup database rutin

---

## 📊 ESTIMASI BIAYA

### FREE Tier:
- **Vercel**: Frontend unlimited
- **Railway**: 500 jam/bulan (≈20 hari non-stop)
- **Total**: $0/bulan ✅

### Paid Tier:
- **Railway Pro**: $5/bulan (unlimited hours)
- **Render**: $7/bulan (backend + db)
- **Digital Ocean**: $6-12/bulan (full control)

---

## 🚀 QUICK START - Deploy ke Railway + Vercel

Mau saya buatkan step-by-step detailed guide untuk Railway + Vercel?
Atau mau saya buatkan Docker setup?

**Pilih platform yang Anda mau, saya bisa bantu setup lengkap!** 🎯
