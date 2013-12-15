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

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.root_block = None
        self.curr_block = None
    
    
    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        for attr in attrs:
            #print "    attr:", attr
            pass
        if is_tag_not_close(tag) == False:
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
        #print "End tag:", tag
        if is_tag_not_close(tag) == False:
            if tag != self.curr_block.name:
                print self.curr_block.name + "not close"
            self.curr_block = self.curr_block.parent_block

    def handle_data(self, data):
        #print "Data:", data
        pass
        
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





file_path = sys.argv[1]

fp = open(file_path, 'r')
html_string = fp.read()
fp.close()

parser.feed(html_string)

block = parser.root_block
print block
