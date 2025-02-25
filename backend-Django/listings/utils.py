import qrcode  # Add this import
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def generate_qr_code(slug):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Use the correct URL with the listing slug
    qr.add_data(f'https://khushmonga.com/listings/HomeOpen_Enquiry/?property={slug}')
    qr.make(fit=True)

    # Create an in-memory buffer to save the QR code image
    qr_img_buffer = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(qr_img_buffer)
    qr_img_buffer.seek(0)

    # Create a Django InMemoryUploadedFile from the buffer
    qr_code_file = InMemoryUploadedFile(
        qr_img_buffer,
        None,
        'qr_code.png',
        'image/png',
        qr_img_buffer.getbuffer().nbytes,
        None
    )

    return qr_code_file
