# make a list of assignments and uses at each line
# make an 2d array that at each entry lists that either say
# array elements represent each line of code
# each entry say what is written and what is read

# If label enter ["Label"][#]
# If, if enter   ["IF:read variables]["#"]
# if assignment ["read variables] 
# if goto everything after until a label is dead ["goto"][]

import sys, re, os

# Tokens
class Label:
  number = 0
  lineNumber = 0
  string = "null"
  def __init__(self, n, ln, line):
    self.number = n
    self.lineNumber = ln
    self.string = line

class If:
  gotoLabelNumber = 0
  readVariables = []
  string = "null"
  def __init__(self, ln, rv, line):
    self.gotoLabelNumber = ln
    self.readVariables = rv
    self.string = line

class Assignment:
  variable = "null"
  readVariables = []
  string = "null"
  def __init__(self, v, rv, line):
    self.variable = v
    self.readVariables = rv
    self.string = line

# index is line number, object has relevant information
tokens = []

# label dictionary
labels = {} # special array where index is equal to the label #

# Open File
filename = sys.argv[1]
while(not os.path.isfile(filename)):
  filename = str(raw_input("Path does not exist! Enter new name: "))
print "Analyzing " + filename + ":\n"


###################################
#  MAIN STORE LOOP
###################################


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

      token = If(gotoLine, readVariables, line)
      tokens.append(token)
#      print ">>CREATED TOKEN: IF goto " + token.gotoLabelNumber + " readings> " + str(token.readVariables)

    ## LABEL
    if re.search('^Label[0-9]', line):
      expression = re.search('(?<=Label)\d+', line)
      number = int(expression.group(0))
      token = Label(number, curLine, line)
      tokens.append(token)
      labels[token.number] = token
   #   print ">>CREATED TOKEN: LABEL >" + str(token.number) + " at line" + str(token.lineNumber)
  #    print "INDEX NUMBER IS CORRECT: "+ str(labels[token.number].number)
   
    ## GOTO Statements
    if re.search('^ goto.', line):
      expression = re.search('(?<=Label)\d+', line)
      gotoLine = expression.group(0)
      token = If(gotoLine, None, line)
      tokens.append(token)
 #     print ">>CREATED TOKEN: IF goto " + token.gotoLabelNumber
 
    ## ASSIGNMENT VARIABLES
    if re.search('([a-z]|[A-Z]) := .*', line):
      variable = re.search('([a-z]|[A-Z])', line).group(0)
      expression = re.findall('([a-z]|[A-Z])', line)
      if expression is not None:
        expression.remove(expression[0])
      readVariables = []
      readVariables.extend(expression)

      token = Assignment(variable, readVariables, line)
      tokens.append(token)
#      print ">>CREATED TOKEN: VARIABLE: ASSIGNED>" + token.variable + " reading>" + str(token.readVariables)
    curLine += 1
    if re.search('#', line):
      expression = re.findall('([a-z]|[A-Z])', line)
      token = Assignment("LAST", expression, line)
      tokens.append(token)

################################
#  MAIN ANALYSIS LOOP
##############################

# Create array to store all strings to be printed, sized 2N+1
# GOING BACKWARDS
# last entry should be comment and every other as well, so 
# reverse the printout array

# Once clobbered, dead until read

alive = set()
printoutArray = []
#printoutArray.append("# ");
for token in reversed(tokens):

# IF STATMENT TOKEN
#  if isinstance(token, If):
     



# LABEL STATMENT TOKEN
#  if isinstance(token, Label):
    


# IF STATMENT TOKEN
  if isinstance(token, Assignment):
  #IF IN SET OF CURRENTLY LIVE VARIABLES, REMOVE WHAT IS ASSIGEND AND ADD WHAT IS READ
    if token.variable in alive:
      alive.remove(token.variable)
    for variable in token.readVariables:
      alive.add(variable)  # add each read variable to being alive at this point
# Finally add the aliveness and token to the prinout array
  if(not "#" in token.string):  
    printoutArray.append(token.string.rstrip())
  printoutArray.append("# " + ", ".join(sorted(alive)))

printoutArray.reverse()

for i in printoutArray:
  print(i)
  
        








# EXAMPLE TOKEN: entry = Assignment("x", "xyz")




 
