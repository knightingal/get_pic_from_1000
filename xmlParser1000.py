class stNode(object):
    pass

def openXmlFile(fileName):
    fd = open(fileName, "r")
    xmlString = fd.read()
    return xmlString

def getNodeByName(xmlString, nodeName):
    
    tailPos = 0
    
    nodeList = []
    nextBeginPos = 0
    
    searchBeg = '<' + nodeName
    
    beginPos = xmlString.find(searchBeg, 0)
    while True:
        if beginPos < 0:
            break
        node = stNode()
        
        
        
        nextBeginPos = xmlString.find(searchBeg, beginPos + 1)
        searchTail = '>'
        tailPos = xmlString.find(searchTail, beginPos)
        if tailPos < 0:
            print "error!"
            break
        nodeAttrString = xmlString[beginPos + len(searchBeg): tailPos]
        node.attrString = nodeAttrString
        node.attrMap = getAttrMap(nodeAttrString)
        if xmlString[tailPos -1] != '/' and nodeName != 'img':
            searchTail = '</' + nodeName + '>'
            tailPos = xmlString.find(searchTail, beginPos)
            if tailPos < 0 or (tailPos > nextBeginPos and nextBeginPos > 0):
                print "error, node in %d not closed" % beginPos
                node.elenString = "no elenString"
            else:
                nodeElenString = xmlString[beginPos : tailPos + len(searchTail)]
                node.elenString = nodeElenString
        else:
            node.elenString = ""
        nodeList.append(node)
        beginPos = nextBeginPos
    return nodeList
        
            
        
        
    


        
errorStat = 0
spaceStat = 1
attNaStat = 2
equalStat = 3
quotaStat = 4
attVaStat = 5

findSpaceCh = 0
findQuotaCh = 1
findEqualCh = 2
findOtherCh = 3

def getCharType(currCh):
    if currCh == '"':
        return findQuotaCh
    elif currCh == ' ':
        return findSpaceCh
    elif currCh == '=':
        return findEqualCh
    else:
        return findOtherCh

class Actions(object):
    def __init__(self, attrString):
        Actions.onIntoAttrNa    = OnIntoAttrNa(attrString)
        Actions.onOutAttrNa     = OnOutAttrNa(attrString)
        Actions.onIntoAttrVa    = OnIntoAttrVa(attrString)
        Actions.onOutAttrVa     = OnOutAttrVa(attrString)
        Actions.onDoNothing     = OnDoNothing(attrString)
        Actions.onError         = OnError(attrString)
        
        
        
class CAttrAction(object):    
    def __init__(self, attrString):
        CAttrAction.attrString = attrString
        CAttrAction.attrMap = {}
    def doAction(self, index):
        pass
    
class OnIntoAttrNa(CAttrAction):
    def doAction(self, index):
        CAttrAction.attrNaBegPos = index
        
class OnOutAttrNa(CAttrAction):
    def doAction(self, index):
        CAttrAction.attrNaEndPos = index
        CAttrAction.attrName = CAttrAction.attrString[CAttrAction.attrNaBegPos : CAttrAction.attrNaEndPos]
        #print "attrName = %s" % CAttrAction.attrName
        
class OnIntoAttrVa(CAttrAction):
    def doAction(self, index):
        CAttrAction.attrVaBegPos = index
        
class OnOutAttrVa(CAttrAction):
    def doAction(self, index):
        CAttrAction.attrVaEndPos = index
        CAttrAction.attrValue = CAttrAction.attrString[CAttrAction.attrVaBegPos : CAttrAction.attrVaEndPos]
        #print "attrValue = %s" % CAttrAction.attrValue
        CAttrAction.attrMap[CAttrAction.attrName] = CAttrAction.attrValue
        
class OnDoNothing(CAttrAction):
    def doAction(self, index):
        pass
        
class OnError(CAttrAction):
    def doAction(self, index):
        print "[OnError]error in %d" % index
    



def getAttrMap(attrString):
    actions = Actions(attrString)
    
    attrSwitchMap = [
                 #findSpaceCh                        findQuotaCh                    findEqualCh                        findOtherCh
    #errorStat
                 [(errorStat, actions.onError),     (errorStat, actions.onError),       (errorStat, actions.onError),       (errorStat, actions.onError)],
    #spaceStat
                 [(spaceStat, actions.onDoNothing), (errorStat, actions.onError),       (errorStat, actions.onError),       (attNaStat, actions.onIntoAttrNa)],
    #attNaStat
                 [(errorStat, actions.onError),     (errorStat, actions.onError),       (equalStat, actions.onOutAttrNa),   (attNaStat, actions.onDoNothing)],
    #equalStat
                 [(errorStat, actions.onError),     (quotaStat, actions.onDoNothing),   (errorStat, actions.onError),       (attVaStat, actions.onIntoAttrVa)],
    #quotaStat
                 [(spaceStat, actions.onDoNothing), (quotaStat, actions.onOutAttrVa),   (errorStat, actions.onError),       (attVaStat, actions.onIntoAttrVa)],
    #attVaStat
                 [(spaceStat, actions.onOutAttrVa), (quotaStat, actions.onOutAttrVa),   (attVaStat, actions.onDoNothing),   (attVaStat, actions.onDoNothing)]   
                 ]
    currStat = spaceStat
    for index in range(0, len(attrString)):
        charType = getCharType(attrString[index])
        nextStat = attrSwitchMap[currStat][charType][0]
        attrSwitchMap[currStat][charType][1].doAction(index)
        currStat = nextStat
    if currStat == attVaStat:
        actions.onOutAttrVa.doAction(len(attrString))
    return CAttrAction.attrMap
        

#attrMap = getAttrMap('attr1="attr1" attr2="a"')
#print attrMap

def formatBrack(targetString):
    stringList = targetString.split('"')
    for index in range(1, len(stringList), 2):
        stringList[index] = stringList[index].replace('<', '&lt')
        stringList[index] = stringList[index].replace('>', '&gt')
        
    newString = ""
    for index in range(0, len(stringList) - 1):
        newString = newString + stringList[index] + '"'
    newString = newString + stringList[-1]
    
    return newString



    

    
    
    
"""xmlString = '<node attr="1" /><node attr="2">"node insight"</node>'
nodeList = getNodeByName(xmlString, "node")
for node in nodeList:
    print node.nodeString"""
