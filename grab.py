#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
from bs4 import BeautifulSoup
import requests
import unicodedata
from threading import Thread


host = u"d.pr"
dir = u'downloads/'


def rnd():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(4)]
    ret = "".join(lst)
    return ret


def chk():
    while True:
        try:
            path = 'http://%s/%s/%s' % (host, random.choice(string.ascii_lowercase), rnd())
            status = requests.head(path, timeout=10).status_code
            print status
            if status == 200:
                content = requests.get(path).content
                if content.find('<section class="image">') > 0:
                    page = BeautifulSoup(''.join(content))
                    imgalt = page.findAll('section', {'class': "image"})[0].img['alt']
                    print '%s - %s' % (path, imgalt)
                    imgsrc = page.findAll('section', {'class': "image"})[0].img['src']
                    o = open(dir + unicodedata.normalize('NFKD', imgalt.replace(":", "_").replace("\\", "_").replace("/", "_")).encode('utf-8', 'ignore'), 'wb')
                    o.write(requests.get(imgsrc).content)
                    o.close()
                elif content.find('<section class="text note">') > 0:
                    print '%s - text note' % path
                else:
                    print '%s - file' % path
        except BaseException as e:
            print e

if __name__ == "__main__":
    for i in range(15):
        t = Thread(target=chk)
        t.start()
