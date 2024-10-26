from typing import List, Dict
import math

# Fungsi untuk menghitung jarak antara dua titik koordinat (latitude dan longitude)
def haversine(lat1, lon1, lat2, lon2):
    # Radius bumi dalam kilometer
    R = 6371.0  
    # Konversi derajat ke radian
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Jarak dalam kilometer
    distance = R * c
    # Konversi ke meter
    distance_meters = distance * 1000
    return distance_meters

# Fungsi untuk menghitung luas poligon menggunakan Shoelace formula
def calculate_polygon_area(points: List[Dict[str, float]]) -> float:
    n = len(points)
    area = 0.0
    
    for i in range(n):
        x1 = points[i]["longitude"]
        y1 = points[i]["latitude"]
        x2 = points[(i + 1) % n]["longitude"]
        y2 = points[(i + 1) % n]["latitude"]
        area += x1 * y2 - x2 * y1
    
    return abs(area) / 2.0
