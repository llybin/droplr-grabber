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
            path = u'http://' + host + u"/c/" + rnd()
            status = requests.head(path, timeout=10).status_code
            if status == 200:
                content = requests.get(path, timeout=10).content
                if content.find('<section class="image">') > 0:
                    page = BeautifulSoup(''.join(content))
                    imgalt = page.findAll('section', {'class': "image"})[0].img['alt']
                    print imgalt
                    imgsrc = page.findAll('section', {'class': "image"})[0].img['src']
                    o = open(dir + unicodedata.normalize('NFKD', imgalt.replace(":", "_").replace("\\", "_").replace("/", "_")).encode('utf-8', 'ignore'), 'wb')
                    o.write(requests.get(imgsrc).content)
                    o.close()
                elif content.find('<section class="text note">') > 0:
                    print path + ' - text note'
                else:
                    print path + ' - file'
        except BaseException:
            pass


if __name__ == "__main__":
    for i in range(30):
        t = Thread(target=chk)
        t.start()
