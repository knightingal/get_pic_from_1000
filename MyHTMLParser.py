from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import sys

class Block(object):
    def __init__(self):
        self.name = ""
        self.child_blocks = []
        self.parent_block = None

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.root_block = None
        self.curr_block = None
    
    
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "    attr:", attr
        if self.root_block == None:
            self.root_block = Block()
            self.root_block.name = tag
            self.curr_block = self.root_block
        else:
            tmp_block = Block()
            tmp_block.name = tag
            tmp_block.parent_block = self.curr_block
            self.curr_block.child_blocks.append(tmp_block)
            self.curr_block = tmp_block
            
            

    def handle_endtag(self, tag):
        print "End tag:", tag
        self.curr_block = self.curr_block.parent_block

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
print html_string
#print html_string
#parser.feed('<div><p>fdf</p><div><p>aaaa</p></div></div>')
parser.feed(html_string)

block = parser.root_block
print block
