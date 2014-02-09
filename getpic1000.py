import sys
from xmlParser1000 import *
import urllib2
import os

rootDirString = '/home/knightingal/Downloads/.mix/1000/'


def isEnChar(char):
    if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z'):
        return True
    else:
        return False


def getpicfrom1000(webpageurl):
    webpagefd = urllib2.urlopen(webpageurl)
    xml_string = webpagefd.read()
    
    new_string = formatBrack(xml_string)
    
    title_node_list = getNodeByName(new_string, "title")
    for node in title_node_list:
        print "title = %s" % node.elenString
        beginpos = node.elenString.find('>')
        beginpos += 1
        endpos = node.elenString.find('[', beginpos)
        if endpos < 0:
            endpos = node.elenString.find('-', beginpos)
        endpos -= 1
        namestring = node.elenString[beginpos : endpos + 1]
        dirstring = namestring.decode("gbk")
        print dirstring
        try:
            os.mkdir(rootDirString + dirstring)
        except OSError:
            print rootDirString + dirstring + "exists"
            

    table_list = getNodeByName(new_string, "table")
    for table in table_list:
        if table.attrMap['cellspacing'] == '2' and table.attrMap['cellpadding'] == '1':
            tr_list = getNodeByName(table.elenString, 'td')
            tr = tr_list[3]
            if tr.elenString.find(namestring) > 0:
                herf_list = getNodeByName(tr.elenString, 'a')
                for href in herf_list:
                    nexturl = "http://www.1000rt.com/" + href.attrMap['href']
            else:
                nexturl = ""
    node_list = getNodeByName(new_string, "p")

    for node in node_list:
        img_node_list = getNodeByName(node.elenString, 'img')
        for imgNode in img_node_list:
            print imgNode.attrMap['src']
            request=urllib2.Request(imgNode.attrMap['src'])
            request.add_header("Referer", webpageurl)       
            request.add_header("User-Agent",
                               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 "
                               "(KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31")
            request.add_header("Connection", "keep-alive")
            request.add_header("Accept", "*/*")
            request.add_header("Accept-Encoding", "gzip,deflate,sdch")
            request.add_header("Accept-Language", "zh-CN,zh;q=0.8")
            request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
            thread = MyThread(request,  dirstring, imgNode.attrMap['src'].split('/'))
            thread.start()
    if nexturl != "":
        getpicfrom1000(nexturl)
        
from threading import Thread


class MyThread(Thread):
    def __init__(self, request, dirstring, stringlist):
        Thread.__init__(self)
        self.request = request
        self.dirstring = dirstring
        self.stringlist = stringlist
    
    def run(self):
        picfd = urllib2.urlopen(self.request)
        picstring = picfd.read()
        picfd.close()
        picfd = open('/home/knightingal/Downloads/.mix/1000/' + self.dirstring + '/' + self.stringlist[-1], 'w')
        picfd.write(picstring)
        picfd.close()
        print self.stringlist[-1] + " done"

if __name__ == "__main__":
    web_url_address = ""
    if len(sys.argv) != 2:
        print "please input web url address..."
        web_url_address = raw_input()
    else:
        web_url_address = sys.argv[1]

getpicfrom1000(web_url_address)
