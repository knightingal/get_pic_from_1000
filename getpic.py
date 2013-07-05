from xmlParser import *
#from urllib2 import *
import urllib2

linkString = ""
webpagefd = urllib2.urlopen(linkString)
xmlString = webpagefd.read()
print "download web page succ"
webpagefd.close()


#xmlString = openXmlFile("/home/knightingal/viewthread.php?tid=939780")




newString = formatBrack(xmlString)

imgString = ""
nodeList = getNodeByName(newString, "div")
for node in nodeList:    
    if 'class' in node.attrMap and node.attrMap['class'] == 't_msgfont':        
        #print node.elenString
        imgString = node.elenString
        
nodeList = getNodeByName(imgString, "img")
for node in nodeList:
    #print node.attrMap["src"]
    url = node.attrMap["src"]
    pos = url.rfind('/')
    fileName = url[pos + 1 : ]
    picfd1 = urllib2.urlopen(url)
    picfd2 = open("/home/knightingal/" + fileName, 'w')
    picdata = picfd1.read()
    picfd2.write(picdata)
    print "%s download" % fileName
    picfd1.close()
    picfd2.close()
    
        
        
