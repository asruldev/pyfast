from fastapi import APIRouter, HTTPException
from data.quran import SURAT_DATA

router = APIRouter(
    prefix='/quran',
    tags=['Al Quran']
)

@router.get("/surat/{surat_id}")
async def get_surat(surat_id: str):
    surat = SURAT_DATA.get(surat_id)
    if surat is None:
        raise HTTPException(status_code=404, detail="Surat tidak ditemukan")
    return surat

@router.get("/surat")
async def get_all_surats():
    return SURAT_DATA