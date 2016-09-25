from PIL import Image
import Image
import os
import glob

# Installing necessary bullshit. Please use Linux to make it good.
os.system("sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl")
os.system("sudo apt-get install ffmpeg")
os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")

# Downloads the video
link = open("link.txt", "w").read()
os.system("youtube-dl -o '%(id)s' https://www.youtube.com/watch?v=" + link)

# Splits the .mp4 video into many .png frames
os.system("ffmpeg -i "link".mp4 -r 60 -s 1920x1080 -f image2 frame-%07d.png")

# Splits each frame into its 60 QR codes and processes them.
lastFrameNumber = max(glob.iglob('*.[Mm][Pp]4'), key=os.path.getctime)
lastFrameNumber = lastFrameNumber[6:13]
for x in (0 to lastFrameNumber):

