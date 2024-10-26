from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter(
    prefix='/shio',
    tags=['Shio']
)

# Data Shio
SHIO_INFO = {
    0: "Monyet",
    1: "Ayam",
    2: "Anjing",
    3: "Babi",
    4: "Tikus",
    5: "Kerbau",
    6: "Macan",
    7: "Kelinci",
    8: "Naga",
    9: "Ular",
    10: "Kuda",
    11: "Domba",
}

@router.get("/{year}")
async def get_shio(year: int):
    if year < 0:
        raise HTTPException(status_code=400, detail="Tahun tidak valid")

    shio_index = year % 12  # Menghitung indeks shio berdasarkan tahun
    shio_name = SHIO_INFO[shio_index]
    
    return {
        "year": year,
        "shio": shio_name
    }

# Data Zodiak
ZODIAK_INFO = {
    "Aries": (datetime(1, 3, 21), datetime(1, 4, 19)),
    "Taurus": (datetime(1, 4, 20), datetime(1, 5, 20)),
    "Gemini": (datetime(1, 5, 21), datetime(1, 6, 20)),
    "Cancer": (datetime(1, 6, 21), datetime(1, 7, 22)),
    "Leo": (datetime(1, 7, 23), datetime(1, 8, 22)),
    "Virgo": (datetime(1, 8, 23), datetime(1, 9, 22)),
    "Libra": (datetime(1, 9, 23), datetime(1, 10, 22)),
    "Scorpio": (datetime(1, 10, 23), datetime(1, 11, 21)),
    "Sagitarius": (datetime(1, 11, 22), datetime(1, 12, 21)),
    "Capricorn": (datetime(1, 12, 22), datetime(1, 1, 19)),
    "Aquarius": (datetime(1, 1, 20), datetime(1, 2, 18)),
    "Pisces": (datetime(1, 2, 19), datetime(1, 3, 20)),
}

@router.get("/zodiak/{day}/{month}")
async def get_zodiak(day: int, month: int):
    # Validasi input tanggal dan bulan
    if month < 1 or month > 12 or day < 1 or day > 31:
        raise HTTPException(status_code=400, detail="Tanggal atau bulan tidak valid")
    
    # Mencari zodiak berdasarkan tanggal
    for zodiak, (start_date, end_date) in ZODIAK_INFO.items():
        start_date = start_date.replace(year=1)  # Mengabaikan tahun
        end_date = end_date.replace(year=1)  # Mengabaikan tahun
        
        if (month == start_date.month and day >= start_date.day) or \
           (month == end_date.month and day <= end_date.day):
            return {
                "zodiak": zodiak
            }
    
    raise HTTPException(status_code=404, detail="Zodiak tidak ditemukan")
