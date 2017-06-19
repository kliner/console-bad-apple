import os
from PIL import Image
import time
import numpy
import mplayer

class VideoConverter(object):

    TEMP = os.path.expanduser('~') + '/.temp/'
    LEN = 219 # length of video(in seconds)
    INTEVAL = 0.1

    def __init__(self):
        self.ids = []
        self.width = 154
        self.height = 45
        self.txtPath = 'ba.txt'

    def parse(self, path):
        self.makeImages(path)
        self.makeTxt()

    def makeImages(self, path):
        c = 0
        t = 0
        while t <= LEN:
            os.system('ffmpeg -i %s -f image2 -ss %s -vframes 1 %s.png' % (path, str(t), self.TEMP + str(c)))
            t += INTEVAL
            self.ids += [c]
            c += 1
            time.sleep(5)

    def makeTxt(self):
        with open(self.txtPath, 'w') as f:
            for c in xrange(int(self.LEN / self.INTEVAL)): 
                im = Image.open(self.TEMP + str(c) + '.png').convert('L')
                im = im.resize((self.width, self.height))
                
                w, h = im.size
                data = numpy.array(im)[:h, :w]
                for row in data:
                    for p in row:
                        if p > 0xdf: f.write(' ')
                        elif p > 0xcf: f.write('.')
                        elif p > 0xbf: f.write(':')
                        elif p > 0xaf: f.write(';')
                        elif p > 0x9f: f.write('!')
                        elif p > 0x8f: f.write('|')
                        elif p > 0x7f: f.write('}')
                        elif p > 0x6f: f.write('T')
                        elif p > 0x5f: f.write('[')
                        elif p > 0x4f: f.write('H')
                        elif p > 0x3f: f.write('X')
                        elif p > 0x2f: f.write('0')
                        elif p > 0x1f: f.write('&')
                        else: f.write('#')
                    f.write('\n')
                f.write(chr(0x1))

class Player(object):

    def __init__(self):
        self.loadTxt('ba.txt')

    def playMusic(self, path):
        p = mplayer.Player('-novideo')
        p.volume = 10
        p.stop()
        p.loadfile(path)
        time.sleep(1)
        p.pause()
        self.p = p

    def loadTxt(self, path):
        with open(path, 'r') as f: self.ss = f.read().split(chr(0x1))

    def play(self):
        self.playMusic("./video.mp4")
        start = time.time()
        while time.time() < start + 219:
            #print("\033c")
            i = int((time.time() - start) * 10)
            print self.ss[i]
            time.sleep(0.09)


if __name__ == '__main__':

    vc = VideoConverter()
    vc.makeTxt()
    p = Player()
    p.play()
