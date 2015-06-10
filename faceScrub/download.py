import os
import urllib
import urllib2
from urllib2 import URLError
import hashlib

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

def getResourceLength(url):
    try:
        response = urllib2.urlopen(HeadRequest(url))
        return response.info().getheader('Content-Length')
    except URLError, e:
        if hasattr(e,'reason'):
            print 'cannot reach a server..\n'
        elif hasattr(e,'code'):
            print 'find http error..\n.'
        else:
            print 'unkown error...\n'
        return ''

def getSha256(filename):
    f = open(filename, 'rb')
    mysha256 = hashlib.sha256()
    mysha256.update(f.read())
    f.close()
    return mysha256.hexdigest()

fid = open("./faceScrub/facescrub_actors.txt", "r")
log = open("./faceScrub/log.txt", "wt")
list = open('./faceScrub/list.txt', 'wt')
line = fid.readline()
count = 1
while line:
    line = fid.readline()
    tmp = line.split("\t")
    file = tmp[0]
    file = file.replace(' ', '_')
    url = tmp[3]
    fr = tmp[4]
    tmp_url = url.split('.')
    sha256 = tmp[5]
    sha256 = sha256.replace('\n', '')
    file_path = './faceScrub/image/'+file
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        count = 1
    response = getResourceLength(url)
    if len(response):
        image_path = file_path+'/'+file+str(count)+'.'+tmp_url[-1]
        print url + ' downloading...'
        urllib.urlretrieve(url, image_path)
        count = int(count) + 1
        img_sha256 = getSha256(image_path)
        if img_sha256 == sha256:
            print url + ' download success..\n'
            list.write(image_path + ' ' + fr + '\n')
            log.write(url + ' download success..\n')
        else:
            print url + ' download error..\n'
            log.write(url + ' download error..\n')
    else:
        print url+ ' not exit..'
        log.write(url + ' not exit..\n')
		
list.close()
log.close()
fid.close()


