from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import sys



class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "    attr:", attr

    def handle_endtag(self, tag):
        print "End tag:", tag

    def handle_data(self, data):
        print "Data:", data
        
    def handle_comment(self, data):
        print "Comment: ",data
        
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Name ent:", c
        
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
            
        print "Num ent:", c
        
    def handle_decl(self, data):
        print "Decl:", data


parser = MyHTMLParser()





file_path = sys.argv[1]

fp = open(file_path, 'r')
html_string = fp.read()
fp.close()
#print html_string
parser.feed(html_string)