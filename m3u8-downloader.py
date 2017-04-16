#!/usr/bin/env python
import os
import sys
import glob
import natsort
import shutil

def main(args):
    outfile = 'outputbymisha.mp4'
    arg1 = args[0]
    if len(args) > 1:
        outfile = args[1]

    pre = arg1[:arg1.rindex('/')+1]

    os.system("curl "+arg1+" > list.txt")
    with open('list.txt', 'r') as f:
        #iterate through each line in the file
        line = f.readline()
        while line.startswith("#"):
            line = f.readline()

    os.system("download-m3u8 "+pre+line)

    tsFiles=[]
    for root, dirs, files in os.walk('./'):
        for myFile in files:
            if myFile.endswith('.ts'):
                tsFiles.append(os.path.join(root, myFile))

    l = list(map(lambda x: "file '" + x + "'", tsFiles))
    sortedl = natsort.natsorted(l)

    outString = '\n'.join(sortedl)

    #write output string to outfile
    with open('./temp.txt', 'w') as of:
        of.write(outString)

    os.system("ffmpeg -f concat -safe 0 -i temp.txt -bsf:a aac_adtstoasc -vcodec copy "+outfile)

    filepath = tsFiles[0]
    afs = filepath[filepath.index('/')+1:]
    afs = afs[:afs.index('/')+1]
    print "removing "+afs+"..."
    shutil.rmtree('./'+afs+'/')
    print "done."


if __name__ == '__main__':

    sys.exit(main(sys.argv[1:]))
