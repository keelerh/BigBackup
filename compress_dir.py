from PIL import Image
import qrcode
import tarfile
import gzip

MAX_DATA_PER_QR = 2900
QR_CODES_PER_FRAME = 60
YOUTUBE_VIDEO_DIMENSIONS = (1920, 1080)
BLOCKSIZE = 1 << 16  # 64kB


def gzipfile(iname, oname, level):
    with open(iname, 'rb') as f_in:
        f_out = gzip.open(oname, 'wb', level)
        while True:
            block = f_in.read(BLOCKSIZE)
            if block == '':
                break
            f_out.write(block)
        f_out.close()
    return


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
    for i, qr in enumerate(qr_codes):
        qr.save("qr" + i + ".png")
    return qr_codes


def stitch_images(image_files):
    canvas = Image.new('RGB', YOUTUBE_VIDEO_DIMENSIONS)
    image_count = 0
    frames = []
    while image_count < len(image_files):
        for i in xrange(0, 1100, 100):
            for j in xrange(0, 700, 100):
                im = image_files[i]
                im.thumbnail(100, 100)
                canvas.paste(im, (i, j))
                image_count += 1
                if image_count >= len(image_files):
                    break
        frames.append(canvas)
        canvas = Image.new('RGB', YOUTUBE_VIDEO_DIMENSIONS)
        for i, qr in enumerate(frames):
            qr.save("frame" + i + ".png")
    return frames


#def convert_to_video(image_files):  #TODO


if __name__ == '__main__':
    gzipfile('6.172.zip', 'gzip_is_cooler', 9)
    compressed_images = qr_encode('6.172.zip')
    frames = stitch_images(compressed_images)
    print frames
#    video_file = convert_to_video(frames)
    # upload to youtube
