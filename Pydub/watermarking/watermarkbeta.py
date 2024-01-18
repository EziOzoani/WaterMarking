from pydub import AudioSegment
import os
import time
import sys

#watermarkbeta.py, or whatever name you want to use
#Python audio watermarking script that takes
#one argument (the name of the audio file being watermarked)
#overlays a second audio file over the beginning and outputs
#it to a destination folder/file
#requires Pydub and ffmpeg libraries/frameworks

rawcom = sys.argv[0]
print("Now watermarking audio file : ", rawcom)
time.sleep (3)

commercial = AudioSegment.from_mp3 (rawcom)
watermrk = AudioSegment.from_mp3("/Users/ezi/Desktop/Audio/pydub/Test_watermark/watermarking/watermark.mp3")

#Lines 10-13, 19 are optional, specific to my implementation
#intro = watermrk (:2750)
##mrk = watermrk (2900:) 
#output1 = intro + commercial 
#output2 = output1.overlay (mrk, position = 3200)
#But if you would like to play with splitting audio, try them out

output1 = commercial.overlay(watermrk, position = 200)
(outputpath, outputfile) = os.path.split (rawcom)
print(outputfile)

dest = os.path.join ('/Users/ezi/Desktop/Audio/pydub/Test_watermark/watermarked','Copr-' + outputfile)
output1.export (dest, format = "mp3")
#output2.export (dest, format = "mp3")

sys.exit()