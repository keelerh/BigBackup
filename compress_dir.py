import Image
import os
import qrcode


# no currently implemented recrusively, only direct children
def compress_files(directory):
    compressed_images = []
    for filename in os.listdir(directory):
        # path = os.path.join(directory, filename)
        img_file = qr_encode(filename)
        compressed_images.append(img_file)
    stitch_images(compressed_images)


def qr_encode(filename):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    qr.add_data(filename.readlines())
    qr.make(fit=True)
    img_file = qr.make_image()
    return img_file


def stitch_images(image_files, n):  # where n is number of QR codes per frame
    i = 0
    while i < len(image_files):
        # stitch images
        i += n


def convert_to_video():
