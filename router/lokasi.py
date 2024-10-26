from fastapi import APIRouter, HTTPException
from helpers.coordinate import haversine, calculate_polygon_area
from typing import List, Dict

router = APIRouter(
    prefix='/location',
    tags=['Lokasi']
)

# Lokasi kantor yang menjadi pusat absensi (misalnya: rumah TSI)
OFFICE_LATITUDE = -6.209736
OFFICE_LONGITUDE = 106.832079

# Endpoint untuk melakukan absensi
@router.post("/absensi")
async def absensi(latitude: float, longitude: float):
    # Hitung jarak antara pengguna dan lokasi kantor
    distance = haversine(latitude, longitude, OFFICE_LATITUDE, OFFICE_LONGITUDE)
    
    # Jika jaraknya lebih dari 30 meter, tolak absensi
    if distance > 30:
        raise HTTPException(status_code=400, detail=f"Anda berada di luar radius absensi yang diizinkan. Jarak: {distance:.2f} meter")
    
    # Jika dalam radius, izinkan absensi dan tampilkan jarak
    return {
        "status": "Absensi berhasil",
        "jarak": f"{distance:.2f} meter"
    }

# Endpoint untuk menghitung luas wilayah
@router.post("/calculate_area")
async def calculate_area(points: List[Dict[str, float]] = [
    {"latitude": -6.9026259, "longitude": 106.7206273},
    {"latitude": -6.5000000, "longitude": 107.8000000},
    {"latitude": -6.3000000, "longitude": 108.7000000},
    {"latitude": -6.8026259, "longitude": 109.7206273}
]):
    # Validasi bahwa ada setidaknya 3 titik
    if len(points) < 3:
        raise HTTPException(status_code=400, detail="Minimal 3 titik diperlukan untuk membentuk poligon.")
    
    # Hitung luas
    area = calculate_polygon_area(points)
    
    return {
        "luas_wilayah": f"{area:.2f} meter persegi"
    }