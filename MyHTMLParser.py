from HTMLParser import HTMLParser

from htmlentitydefs import name2codepoint
import sys

tag_not_close = ['img', 'link', 'input', 'p', 'br', 'meta']

def is_tag_not_close(tag_name):
    return tag_name in tag_not_close

class Block(object):
    def __init__(self):
        self.name = ""
        self.child_blocks = []
        self.parent_block = None
        self.attrs = []
        self.data = ""
        
    

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.root_block = None
        self.curr_block = None
    
    
    def handle_starttag(self, tag, attrs):
#        print "Start tag:", tag
        for attr in attrs:
            #print "    attr:", attr
            pass
        if is_tag_not_close(tag) == False:
            if self.root_block == None:
                self.root_block = Block()
                self.root_block.name = tag
                self.root_block.attrs = attrs
                self.curr_block = self.root_block
            else:
                tmp_block = Block()
                tmp_block.name = tag
                tmp_block.attrs = attrs
                tmp_block.parent_block = self.curr_block
                self.curr_block.child_blocks.append(tmp_block)
                self.curr_block = tmp_block
        if tag == "img" and self.curr_block.name == "a" and self.curr_block.parent_block.name == "td":
            print self.curr_block.attrs[1][1]
            print self.curr_block.attrs[0][1]

    def handle_endtag(self, tag):
#        print "End tag:", tag
        if is_tag_not_close(tag) == False:
            if tag != self.curr_block.name:
                print self.curr_block.name + "not close"
            self.curr_block = self.curr_block.parent_block

    def handle_data(self, data):
#        print "Data:", data
        if self.curr_block != None and self.curr_block.name == 'a':
            self.curr_block.data = data
            #print 'a tag data = ' + data
        
    
        
    def handle_comment(self, data):
        #print "Comment: ",data
        pass
        
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #print "Name ent:", c
        
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
            
        #print "Num ent:", c
        
    def handle_decl(self, data):
        #print "Decl:", data
        pass
    
parser = MyHTMLParser()

import urllib2

file_path = sys.argv[1]
if file_path.find("http://") == -1:
    fp = open(file_path, 'r')
else:
    fp = urllib2.urlopen(file_path)
html_string = fp.read()
fp.close()
#html_string = "<div>fjaldjf</div>"
dirstring = html_string.decode("gbk")
#print dirstring
parser.feed(dirstring)

block = parser.root_block
print block
