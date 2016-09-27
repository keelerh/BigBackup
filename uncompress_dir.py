"""

Please run the following commands (or your OS's variant of these commands).

You need these things installed.

sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl

sudo apt-get install ffmpeg

sudo apt-get install python-qrtools

"""

import qrcode
import sys
import os
import glob
import tarfile
import qrcode
import subprocess


MAX_DATA_PER_QR = 2700

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, source_dir)


def qr_encode(zipped_dir):
    qr_codes = []
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
    bytesread = 0
    with open(zipped_dir, 'r') as f:
        for line in f:
            print str(bytesread) + " bytes read..."
            bytesread += len(line)
            if bytesread >= MAX_DATA_PER_QR:
                print "QR code generated"
                try:
                    bytesread -= len(line)
                    qr.make(fit=True)
                    img_file = qr.make_image()
                    qr_codes.append(img_file)
                except:
                    pass
                qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                      )  # reset qr code generator
                bytesread = len(line)  # reset size count
                bytesread = 0
            qr.add_data(line)
    if bytesread > 0:
        qr.make(fit=True)
        img_file = qr.make_image()
        qr_codes.append(img_file)
        print "QR code generated"
    max_len = len(str(len(qr_codes)))
    print str(len(qr_codes)) + " frames in total..."
    for frame, code in enumerate(qr_codes):
        code.save("frame-" + str(frame).zfill(max_len) + ".png")
    return qr_codes


def convert_to_mp4(image_files, output_filename):
    subprocess.call(['ffmpeg', '-r', '1', '-s', '177x177',
                     '-i', 'frame-%d.png', 'backup.mp4'])

# Downloads the video
# link = open("link.txt", "r").read()
# os.system("youtube-dl -o '%(id)s' http://www.youtube.com/watch?v=" + link)

# videoName = "'" + link + ".mp4'"

#def retrieve_frames(video_file):
# Splits the .mp4 video into many .png frames
       # os.system("ffmpeg -i " + video_file + " -r 1 -s 177x177 -f image2 frame-%07d.png")


# Processes each frame and appends the data to storage.tar
#lastFrameNumber = max(glob.iglob('*.[Mm][Pp]4'), key=os.path.getctime)
#print(lastFrameNumber)
#lastFrameNumber = lastFrameNumber[6:13]
#for frame in range(1, (int(lastFrameNumber) + 1)):

def convert_from_mp4(output_filename):
    subprocess.call(['ffmpeg', '-i', 'backup.mp4', '-s', '177x177', '-f',
    'image2', 'frame-%d.png'])


def post_process_frames():
    # The .tar where things are stored
    storage = open("storage.tar", "w+")
    for frame in range(6):
        d = qrcode.Decoder()
        framePath = str(frame) + ".png"
        fullFramePath = "frame-" + framePath.zfill(11)
        d.decode(fullFramePath)
        print(d.result)
        storage = open("storage.tar", "a+")
        storage.write(d.result)


def prepare_user_content(path):
    make_tarfile('tmp', path)
    # encrypt_tar('test', 'test', 'public_key')
    # os.system('storage.tar')
    compressed_images = qr_encode('tmp')
    convert_to_mp4(compressed_images, 'backup.mp4')
    convert_from_mp4('backup.mp4')
#    post_process_frames()

print "Video successfully uploaded to YouTube"
