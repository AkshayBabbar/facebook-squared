import serial
from urllib2 import urlopen
from simplejson import loads
import fbconsole
import serial
import time
from api import *
import Image
import urllib

#content = loads(urlopen('http://graph.facebook.com/jpwright').read())
#print content

fbconsole.AUTH_SCOPE = ['read_stream']
fbconsole.authenticate()
print "authenticated"

port = "/dev/pts/5"
#port = "/dev/ttyACM0"
ser = serial.Serial(port, 57600, timeout=1)
print "communicating on "+ser.portstr

print "listening"

bannedTypes = ["photo", "video"]

displaying = "none"

while(1):
    #ser.write("hello")
    #print "hello"
    #time.sleep(0.2)
    line = ser.readline()
    if line.startswith("h"):
        print "hello"
        ser.write("hello")
    if line.startswith("f"):
        newsfeed = fbconsole.get('/me/home')
        newsfeedData = newsfeed["data"]
        nfDataClean = newsfeedData
        it = iter(nfDataClean)
        #for i in range(0, len(newsfeedData)-2): #last entry is paging stuff
        try:
            while 1:
                newsItem = it.next()
                #print newsItem["id"]
                if newsItem["type"] in bannedTypes:
                    newsfeed["data"].remove(newsItem)
        except StopIteration:
            x = 0
        newsfeedstart = 0
        displaying = "feed"
        printnews(newsfeed, newsfeedstart, ser)
        header = ".wt0News Feed\n.wt1----------------"
        ser.write(header)
    if line.startswith("n"):
        if displaying == "feed":
            newsfeedstart += 3
            printnews(newsfeed, newsfeedstart, ser)
            header = ".wt0News Feed\n.wt1----------------"
            ser.write(header)
        if displaying == "post":
            x = 0
            #print comments, tbd
    if line.startswith("p"):
        if(newsfeedstart>0):
            newsfeedstart -= 3
            header = ".wt0News Feed\n.wt1----------------"
            ser.write(header)
        printnews(newsfeed, newsfeedstart, ser)
    if line.startswith("e"):
        num = int(line[1:2])-1
        itemnum = num+newsfeedstart
        printitem(newsfeed, itemnum, ser)
        userid = newsfeed["data"][itemnum]["from"]["id"]
        pictureUrl = fbconsole.graph_url("/"+userid+"/picture")
        urllib.urlretrieve(pictureUrl, "profile.jpg")
        im = Image.open("profile.jpg")
        #print im.format, im.size, im.mode
        bw = im.convert("1")
        bw.save("profile_bw.jpg")
        pix = bw.load()
        imsg = ".i"
        for x in range(0,50):
            for y in range(0,50):
                if pix[y,x] == 255:
                    imsg += "0"
                else:
                    imsg += "1"
        imsg += "\n"
        print "writing image"
        #print imsg
        ser.write(imsg)
        displaying = "post"
        
