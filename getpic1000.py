from xmlParser import *
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
    xmlString = webpagefd.read()
    
    newString = formatBrack(xmlString)
    
    titleNodeList = getNodeByName(newString, "title")
    for node in titleNodeList:
        print "title = %s" % node.elenString
        beginpos = node.elenString.find('>')
        beginpos += 1
        endpos = node.elenString.find('[', beginpos)
        endpos -= 1
        namestring = node.elenString[beginpos : endpos + 1]
        dirstring = namestring.decode("gbk")
        print dirstring
        try:
            os.mkdir('/home/knightingal/Downloads/.mix/1000/' +dirstring)
        except OSError:
            print '/home/knightingal/Downloads/.mix/1000/' + dirstring + "exists"
            

    tableList = getNodeByName(newString, "table")
    for table in tableList:
        if table.attrMap['cellspacing'] == '2' and table.attrMap['cellpadding'] == '1':
            trList = getNodeByName(table.elenString, 'td')
            tr = trList[3]
            if tr.elenString.find(namestring) > 0:
                hrefList = getNodeByName(tr.elenString, 'a')
                for href in hrefList:
                    nexturl = url1000 + href.attrMap['href']
            else:
                nexturl = ""
                        
                    
    

    nodeList = getNodeByName(newString, "p")



    for node in nodeList:
        imgNodeList = getNodeByName(node.elenString, 'img')
        for imgNode in imgNodeList:
            print imgNode.attrMap['src']
            request=urllib2.Request(imgNode.attrMap['src'])
            request.add_header("Referer", webpageurl)       
            request.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31")
            request.add_header("Connection", "keep-alive")
            request.add_header("Accept", "*/*")
            request.add_header("Accept-Encoding", "gzip,deflate,sdch")
            request.add_header("Accept-Language", "zh-CN,zh;q=0.8")
            request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
            
            picfd = urllib2.urlopen(request)
            picstring = picfd.read()
            picfd.close()
            stringlist = imgNode.attrMap['src'].split('/')
            picfd = open('/home/knightingal/Downloads/.mix/1000/' + dirstring + '/' + stringlist[-1], 'w')
            picfd.write(picstring)
            picfd.close()
            
    if nexturl != "":
        getpicfrom1000(nexturl)
        
        
        
import sys, os
getpicfrom1000(sys.argv[1])
