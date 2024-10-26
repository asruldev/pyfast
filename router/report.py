from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from helpers.pdf_file import generate_receipt_pdf

router = APIRouter(
    prefix='/report',
    tags=['Laporan']
)

@router.get("/print-label")
async def print_label():
    # Data pengiriman (seharusnya dari database)
    sender = "Asrul Harahap"
    receiver = "Budi Santoso"
    weight = 1.5
    item_type = "Dokumen"
    tracking_number = "1234567890"

    # Generate PDF untuk resi
    pdf_buffer = generate_receipt_pdf(sender, receiver, weight, item_type, tracking_number)

    # Mengembalikan PDF sebagai StreamingResponse
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=resi-{tracking_number}.pdf"
        # "Content-Disposition": f"inline; filename=resi-{tracking_number}.pdf"
    })
