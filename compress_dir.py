from os import listdir
from os.path import isfile, join
import qrcode


def compress_files(directory):
    filepaths = []
    for root, directories, files in os.walk(directory):
       for filename in files:
            filepath = os.path.join(root, filename)
            filepaths.append(filepath)
    compressed_images = [qr_encode(f) for f in filenames]
    frames = stitch_images(compressed_images)
    video_file = convert_to_video(frames)

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
