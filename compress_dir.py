import Image
import libarchive.public
import libarchive.constants
from os import listdir
from os.path import isfile, join
import qrcode
import libarchive.public
import libarchive.constants
import os


MAX_DATA_PER_QR = 2956
QR_CODES_PER_FRAME = 60
YOUTUBE_VIDEO_DIMENSIONS = (1920, 1080)


def zip_dir(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        filenames.extend([os.path.join(root, f) for f in files])
    zipfile = libarchive.public.create_file(
        'create.7z',
        libarchive.constants.ARCHIVE_FORMAT_7ZIP,
        filenames)
    return zipfile


def qr_encode(zipped_dir):
    qr_codes = []
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    bytesread = 0
    with open(zipped_dir, 'r') as f:
        for line in f:
            bytesread += len(line)
            if bytesread >= MAX_DATA_PER_QR:
                bytesread -= len(line)
                qr.make(fit=True)
                img_file = qr.make_image()
                qr_codes.append(img_file)
                qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                bytesread = len(line)
            qr.add_data(line)
    if bytesread > 0:
        qr.make(fit=True)
        img_file = qr.make_image()
        qr_codes.append(img_file)
    return qr_codes


def stitch_images(image_files):  #TODO
    canvas = Image.new('RGB', YOUTUBE_VIDEO_DIMENSIONS)
    image_count = 0
    frames = []
    for i in xrange(0,1100,100):
        for j in xrange(0,700,100):
            im = image_files[i]
            im.thumbnail(100, 100)
            canvas.paste(im, (i, j))
            image_count += 1
            if image_count >= len(image_files):
                break


def convert_to_video(image_files):  #TODO


if __name__ == '__main__':
    zipped_dir =  # TODO
    compressed_images = qr_encode(zipped_dir)
    frames = stitch_images(compressed_images)
    video_file = convert_to_video(frames)
    # upload to youtube
