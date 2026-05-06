from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import fasilitas, auth, detection
from database import db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database pool
    await db.connect()
    yield
    # Shutdown: Close database pool
    await db.disconnect()

app = FastAPI(
    title="WebGIS API - Tugas Praktikum 10",
    description="API untuk WebGIS dengan Object Detection YOLOv8",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Selamat datang di API WebGIS - Tugas Praktikum 10"}

# Include routers
app.include_router(auth.router)
app.include_router(fasilitas.router)
app.include_router(detection.router)

# Special handling for /geojson
@app.get("/geojson", tags=["Spatial"])
async def get_geojson_root(pool=fasilitas.Depends(fasilitas.get_db)):
    return await fasilitas.get_geojson(pool)
