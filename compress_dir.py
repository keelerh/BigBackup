import qrcode
import tarfile
import subprocess
# import os
# import gnupg

MAX_DATA_PER_QR = 2700
QR_CODES_PER_FRAME = 60
YOUTUBE_VIDEO_DIMENSIONS = (1920, 1080)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, source_dir)


#  def encrypt_tar(output, source, public_key):
#      gpg = gnupg.GPG(public_key)
#      with open('storage.tar', 'rb') as f:
#          status = gpg.encrypt_file(
#              f, recipients=['User'],
#              always_trust='true',
#              output='storage.tar.gpg')


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
                      )  # reset qr code generator
                bytesread = len(line)  # reset size count
            if len(line) > MAX_DATA_PER_QR:
                n = MAX_DATA_PER_QR % len(line)
                for x in xrange(n):
                    qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                          )  # reset qr code generator
                    qr.add_data(line[MAX_DATA_PER_QR / x: MAX_DATA_PER_QR / (x
                                     + 1) - 1])
                bytesread = 0
            else:
                qr.add_data(line)
    if bytesread > 0:
        qr.make(fit=True)
        img_file = qr.make_image()
        qr_codes.append(img_file)
    max_len = len(str(len(qr_codes)))
    for frame, code in enumerate(qr_codes):
        code.save("frame-" + str(frame).zfill(max_len) + ".png")
    return qr_codes


def convert_to_mp4(image_files, output_filename):
    subprocess.call(['ffmpeg', '-r', '1', '-s', '177x177',
                     '-i', 'frame-%d.png', output_filename])


def prepare_user_content(path):
    make_tarfile('tmp', path)
    # encrypt_tar('test', 'test', 'public_key')
    # os.system('storage.tar')
    compressed_images = qr_encode('tmp')
    convert_to_mp4(compressed_images, 'backup.mp4')
