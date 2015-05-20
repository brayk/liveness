import sys, re, os


class Node:
    variable = None
    prev = set()
    value = None
    type = None
    labelNumber = None
    gotoNumber = None
    liveBefore = set()
    liveAfter = set()
    def __init__(self, ln, rv, t):
        self.value = ln
        self.liveBefore = rv
        self.type = t

class Block:
    labelNumber = None
    headNode = None
    tailNode = None
    next = None
    nodes = []


filename = sys.argv[1]

nodes = []
headNodes = {}

curLine = 0
with open(filename, 'r') as f:
    for line in f:
        
        print str(curLine) + '|' + line.rstrip()
    
        ## IF STATEMENTS
        if re.search('^ if.', line):
            expression = re.search('(?<=Label)\d+', line)
            gotoLine = expression.group(0)
                
            expression = re.findall('( [a-z] | [A-Z] )', line)
            readVariables = []
            readVariables.extend(expression)
            
            node = Node(line, expression ,"if")
            node.gotoNumber = gotoLine
            nodes.append(node)
    #      print ">>CREATED TOKEN: IF goto " + token.gotoLabelNumber + " readings> " + str(token.readVariables)

        ## LABEL
        if re.search('^Label[0-9]', line):
            expression = re.search('(?<=Label)\d+', line)
            number = int(expression.group(0))
            print(number)

            node = Node(line, set(), "label")
            node.labelNumber = number
            nodes.append(node)
                #   print ">>CREATED TOKEN: LABEL >" + str(token.number) + " at line" + str(token.lineNumber)
                #    print "INDEX NUMBER IS CORRECT: "+ str(labels[token.number].number)

        ## GOTO Statements
        if re.search('^ goto.', line):
            expression = re.search('(?<=Label)\d+', line)
            gotoLine = expression.group(0)
            node = Node(line, set(), "goto")
            node.gotoNumber = gotoLine
            nodes.append(node)
                #     print ">>CREATED TOKEN: IF goto " + token.gotoLabelNumber

        ## ASSIGNMENT VARIABLES
        if re.search('([a-z]|[A-Z]) := .*', line):
            variable = re.search('([a-z]|[A-Z])', line).group(0)
            expression = re.findall('([a-z]|[A-Z])', line)
            if expression is not None:
                expression.remove(expression[0])
                readVariables = []
                readVariables.extend(expression)
            print(str(expression) + "FUCKING RIGHT HERE")
            node = Node(line, expression, "assign")
            node.variable = variable
            nodes.append(node)
                            #      print ">>CREATED TOKEN: VARIABLE: ASSIGNED>" + token.variable + " reading>" + str(token.readVariables)

        curLine     += 1
        if re.search('#', line):
            expression = re.findall('([a-z]|[A-Z])', line)
            node = Node(line, expression, "LAST")
            nodes.append(node)
        print(str(node.liveBefore))

print(str(len(nodes)) + "***********************")

count = 0
blocks = []
#node previous and block creation, and graph head node look up table FIRST TRAVERSAL
for node in nodes:
    #if(count - 1 >= 0):
    #   node.prev.add(nodes[count-1])
    print(str(node.liveBefore) + " BEFORE UPDATE")
    if(node is nodes[0] and node.type is not "label" and node.type is not "goto" and node.type is not "if"):
        block = Block()
        block.headNode = node
        blocks.append(block)
    if(node.type is "label"):
        block = Block()
        block.labelNumber = node.labelNumber
        if(count + 1 < len(nodes)):
            block.headNode = nodes[count+1]
            headNodes[str(node.labelNumber)] = node

        blocks.append(block)
    if(node.type is "goto" or node.type is "if"):
        block = Block()
        if(count + 1 < len(nodes)):
            block.headNode = nodes[count+1]
        blocks.append(block)
    print(str(node.liveBefore) + " AFTER UPDATE")

    count += 1

#block previous and tail
count = 0
print(headNodes)
nodes.reverse()
for node in nodes:
    if(node.type is "assign"):
        if(count+1 < len(nodes)):
            nodes[count+1].prev.add(node)


    if(node.type is "if"):
        if(count+1 < len(nodes)):
            nodes[count+1].prev.add(node)
            print("GO TO: " + node.gotoNumber)
        headNodes[node.gotoNumber].prev.add(node)

    if(node.type is "goto"):
        headNodes[node.gotoNumber].prev.add(node)
    for after in node.liveAfter:
        if(after not in node.liveBefore and after is not node.variable):
            node.liveBefore.add(after)


    count += 1



#count += 1
#nodes.reverse()

for node in nodes:
    for prevNode in node.prev:
        if(node.variable is not None and node.variable in prevNode.liveAfter):
            prevNode.liveAfter.remove(node.variable)
        if(node.liveBefore is not None):
            print(str(prevNode.liveAfter) + " BEFORE UPDATE")
            for before in node.liveBefore:
                prevNode.liveAfter.add(before)
            print(str(prevNode.liveAfter) + " AFTER UPDATE")

print(nodes[0].prev)
nodes.reverse()
for node in nodes:
    if(node.type is "label"):
        print(node.value.rstrip())
    else:
        if(node.liveBefore is not None):
            print("# " + ", ".join(sorted(node.liveBefore)))
        else:
            print("# hey")
        print(node.value.rstrip())
        if(node.liveAfter is not None):
            print("# " + ", ".join(sorted(node.liveAfter)))
        else:
            print("# ")











