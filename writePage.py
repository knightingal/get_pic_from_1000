# -*- coding: utf-8 -*-  
import os

def writePage(dir):
    fileList = []
    for root, dirs, files in os.walk(dir):
        for fileName in files:
            fileList.append(fileName)
                
    pageString = "<html><head></head><body>"
    for fileName in fileList:
        pageString = pageString + '<img src="' + fileName + '" />'
    pageString = pageString + '</body></html>'
    
    
    pagefd = open(dir + '/page.htm', 'w')
    pagefd.write(pageString)
    pagefd.close()
        
    
    
writePage("/home/knightingal/Downloads/mix/1000/")