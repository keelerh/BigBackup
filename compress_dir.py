from PIL import Image
import qrcode
import tarfile
import subprocess
import os
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
    #  command = [FFMPEG_BIN, '-y',  # (optional) overwrite output file if it exists
    #              '-f', 'rawvideo',
    #              '-vcodec', 'rawvideo',
    #              '-s', '177x177',  # size of one frame
    #              '-pix_fmt', 'rgb24',
    #              '-r', '24',  # frames per second
    #              '-i', '-',  # The imput comes from a pipe
    #              '-an',  # Tells FFMPEG not to expect any audio
    #              '-vcodec', 'mpeg',
    #              output_filename]
    #  pipe = subprocess.Popen(command, stdin=subprocess.PIPE,
    #          stderr=subprocess.PIPE, shell=True)
    #  for image in image_files:
    #      pipe.stdin.write(image.tobytes())
    #  pipe.stdin.close()
    #  pipe.stderr.close()
    subprocess.call(['ffmpeg', '-r', '6', '-s', '177x177',
        '-i', 'frame-0.png', 'test.mp4'])


if __name__ == '__main__':
    make_tarfile('compressed_test', 'test')
#    encrypt_tar('test', 'test', 'public_key')
    #os.system('storage.tar')
    compressed_images = qr_encode('compressed_test')
    # frames = stitch_images(compressed_images)
    convert_to_mp4(compressed_images, 'vid_for_tube.mp4')
