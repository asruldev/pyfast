from io import BytesIO
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  # Untuk membaca gambar dari buffer
import qrcode

# Helper untuk membuat PDF resi
def generate_receipt_pdf(sender, receiver, weight, item_type, tracking_number):
    buffer = BytesIO()
    # Set ukuran halaman untuk printer kecil (contoh: 80mm x 120mm)
    width, height = (80 * mm, 120 * mm)
    c = canvas.Canvas(buffer, pagesize=(width, height))

    # Menulis konten resi ke dalam PDF
    c.drawString(10 * mm, height - 10 * mm, f"Pengirim: {sender}")
    c.drawString(10 * mm, height - 20 * mm, f"Penerima: {receiver}")
    c.drawString(10 * mm, height - 30 * mm, f"Berat: {weight}kg")
    c.drawString(10 * mm, height - 40 * mm, f"Jenis Barang: {item_type}")
    c.drawString(10 * mm, height - 50 * mm, f"Resi: {tracking_number}")

    # Generate QR Code menggunakan qrcode library
    qr_img = qrcode.make(tracking_number)

    # Simpan QR Code ke dalam buffer menggunakan Pillow
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)  # Reset buffer ke awal

    # Gunakan ImageReader untuk membaca gambar dari buffer
    qr_image = ImageReader(qr_buffer)

    # Tambahkan gambar QR Code ke dalam PDF
    c.drawImage(qr_image, 10 * mm, height - 90 * mm, 30 * mm, 30 * mm)

    # Menutup PDF
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer