from xmlParser import *
import urllib2
import os

def isEnChar(char):
    if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z'):
        return True
    else:
        return False

url1000 = ""

def getpicfrom1000(webpageurl):
#webpageurl = "http://www.1000rt.com/News/20121109/101513.htm"
    #xmlString = openXmlFile("/home/knightingal/new470455.htm")
    webpagefd = urllib2.urlopen(webpageurl)
    xmlString = webpagefd.read()
    
    newString = formatBrack(xmlString)
    
    titleNodeList = getNodeByName(newString, "title")
    for node in titleNodeList:
        print "title = %s" % node.elenString
        beginpos = node.elenString.find('>')
        beginpos += 1
        #while isEnChar(node.elenString[beginpos]) == False:
        #    beginpos += 1
        endpos = node.elenString.find('[', beginpos)
        endpos -= 1
        #while isEnChar(node.elenString[endpos]) == True:
        #    endpos += 1
        namestring = node.elenString[beginpos : endpos + 1]
        dirstring = namestring.decode("gbk")
        print dirstring
        try:
            os.mkdir('/home/knightingal/Downloads/.mix/1000/' +dirstring)
        except OSError:
            print '/home/knightingal/Downloads/.mix/1000/' + dirstring + "exists"
            

    tableList = getNodeByName(newString, "table")
    for table in tableList:
        #print table.attrString
        if table.attrMap['cellspacing'] == '2' and table.attrMap['cellpadding'] == '1':
            trList = getNodeByName(table.elenString, 'td')
            tr = trList[3]
            if tr.elenString.find(namestring) > 0:
                hrefList = getNodeByName(tr.elenString, 'a')
                for href in hrefList:
                    nexturl = url1000 + href.attrMap['href']
            else:
                nexturl = ""
                        
                    
                #print tr.elenString
    

    nodeList = getNodeByName(newString, "p")
    #http://531.1000yishu.com/201305/029/1.jpg



    for node in nodeList:
        imgNodeList = getNodeByName(node.elenString, 'img')
    #print node.elenString
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
        
        
        

weburl = ""
getpicfrom1000(weburl)
