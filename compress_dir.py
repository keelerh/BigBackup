from os import listdir
from os.path import isfile, join
import qrcode
import zipfile

    compressed_images = [qr_encode(f) for f in filenames]
    frames = stitch_images(compressed_images)
    video_file = convert_to_video(frames)


def zipdir(directory, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


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


if __name__ == '__main__':
    zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('tmp/', zipf)
    zipf.close()
