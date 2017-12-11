# Programmer:   Jared Strand
# Platform:     Windows
# global variables


###need to fix
#no mas

import re                               #tokenize the code
opStack = []
dictStack = [] #list of int, list tuples
debug_level = 0
scope = ""
static_link_var = 0

#----------------PART 2 BEGIN----------

#Interpreter function accepts
def interpreter(s, scopeInput):
    global scope
    scope = scopeInput
    interpretSPS(parse(tokenize(s)), scope)

def interpretSPS(codeArray, scope):
    #where the magic happens, put stuff on the stacks, s is a code array, scope is 'dynamic' or 'static'
    for token in codeArray:
        if isinstance(token, bool) or isinstance(token, float) or isinstance(token, int) or isinstance(token, list):        #If token is int bool or float we push to the opstack
            opPush(token)
        else:                                                      #If token is not a list(Code Array)
            if token[0] is '/':                                                                     #name of a variable or function needs to be pushed to opstack
                opPush(token)
            elif token[0] is '(':                                                                   #Token is a string, push to opstack
                opPush(token)
            elif token == "add":                                                                    #checks list of built in operators, execute proper operator
                add()
            elif token == "sub":
                sub()
            elif token == "mul":
                mul()
            elif token == "div":
                div()
            elif token == "eq":
                eq()
            elif token == "lt":
                lt()
            elif token == "gt":
                gt()
            elif token == "length":
                length()
            elif token == "get":
                get()
            elif token == "getinterval":
                getinterval()
            elif token == "and":
                psAnd()
            elif token == "or":
                psOr()
            elif token == "not":
                psNot()
            elif token == "if":
                psIf()
            elif token == "ifelse":
                psIfElse()
            elif token == "exch":
                exch()
            elif token == "pop":
                opPop()
            elif token == "roll":
                roll()
            elif token == "copy":
                copy()
            elif token == "clear":
                clear()
            elif token == "dict":
                psDict()
            elif token == "begin":
                begin()
            elif token == "end":
                end()
            elif token == "def":
                psDef()
            elif token == "dup":
                dup()
            elif token == "stack":
                stack()
            else:
                temp_val = lookup(token)                                #Handles tokens if list or none
                if isinstance(temp_val, list) == True:                  #is a code array
                    if scope == "Static":
                        d = {}
                        staticLink = getStaticLink(token)
                        dictStack.append((staticLink, d))
                        interpretSPS(temp_val, scope)
                    else:
                        d = {}                          #need to fix, not done
                        staticLink = getStaticLink(token)
                        dictStack.append((staticLink, d))
                        interpretSPS(temp_val, scope)
                elif temp_val == None:
                    opPush(token)
                else:
                    opPush(temp_val)

def parse(s):               #S is a string of tokens
    #group tokens correctly
    return group(s)

def groupMatching(it):
    res = []                                                    #Make the tokens into code arrays recursively
    for c in it:
        if c == '}':
            return res
        elif c == '{':
            res.append(groupMatching(it))
        else:
            # convert ints bools and floats here
            if is_number(c) == True:
                if float(c) == int(c):
                    c = int(c)
                else:
                    c = float(c)
            elif is_bool(c) == True:
                if c == "true":
                    c = True
                else:
                    c = False
            res.append(c)

    return False

def group(s):
    res = []                                                   #Makes the tokens into parsed code arrays
    it = iter(s)
    for c in it:
        if c == '}':
            return False
        elif c == '{':
            res.append(groupMatching(it))
        else:
            #convert ints bools and floats here
            try:
                c = float(c)
                if c == int(c):
                    c = int(c)
            except ValueError:
                pass

            if is_bool(c) == True:
                if c == "true":
                    c = True
                else:
                    c = False
            res.append(c)

    return res

def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)               #Tokenizes



#---------Helper Functions--------

def is_bool(s):                                 #is bool helper function
    if s == "true" or s == "false":
        return True

    return False

def is_number(s):                               #is number helper function
    try:
        complex(s)
    except ValueError:
        return False

    return True

def getStaticLink(name):
    #get the index where this function is defined
    if(len(dictStack) is 0):
        return 0
    else:
        currentIndex = len(dictStack) - 1 #top of dictstack
    while(1):
        for d in dictStack[currentIndex][1]:
            if dictStack[currentIndex][1].get('/' + name, None) != None:
                return currentIndex
        if (currentIndex is 0):
            return 0
        else:
            currentIndex = dictStack[currentIndex][0]  # set the new index to the currents static link










#---------Conditional Operators--------

def psIf():                                             #Handles if statements on the stack, chooses correct code array based on bool_op variable
    if len(opStack) > 1:
        cond_statement = opPop()
        bool_op = opPop()
        if(bool_op == True):
            interpretSPS(cond_statement)
    else:
        debug("Not enough operands on the stack")

def psIfElse():                                         #Handles ifelse statements on the stack, chooses correct code array based on bool_op variable
    if len(opStack) > 2:
        cond_False_statement = opPop()
        cond_True_statement = opPop()
        bool_op = opPop()
        if(bool_op == True):
            interpretSPS(cond_True_statement)
        elif(bool_op == False):
            interpretSPS(cond_False_statement)
        else:
            debug("Not a good bool")
    else:
        debug("Not enough operands on the stack")





#----------------PART 2 END------------


#--------------------------------


def debug(*s):
    if debug_level > 0:
        print(s)


#---------- Operand Stack Operators --------------
# Pop a value from the opStack
def opPop():
    if len(opStack) > 0:
        x = opStack[len(opStack) - 1]
        opStack.pop(len(opStack) - 1)
        return x
    else:
        debug("Error: opPop - Operand stack is empty")

# Pop a value from the opStack
def opPush(value):
    opStack.append(value)

#---------- Dict Stack Operators ---------------
def dictPop():
    if len(dictStack) > 0:
        dictStack.pop(len(dictStack) - 1)
    else:
        debug("Error: dictPop - Dictionary stack is empty")

def dictPush():
    d = {}
    dictStack.append((0, d))

def define(name, value):
    currentIndex = len(dictStack) - 1
    if (len(dictStack) > 0):
        dictStack[currentIndex][1][name] = value
    else:
        newDict = {}
        newDict[name] = value
        dictStack.append((0, newDict))
    #
    # else:
    #     initialLink = 0
    #     newDict = {}
    #     newDict[name] = value
    #     dictStack.append((initialLink, newDict)) #needs index if static scope

def lookup(name):
    #dictstack looks like this [(link, {dictstuff}), (link to calling, {dictstuff})]
        #follow static link if not in current dict., current dict is top of stack
    currentIndex = len(dictStack) - 1
    name = '/' + name
    while(1):
        for d in dictStack[currentIndex][1]:
            if d == name:
                return dictStack[currentIndex][1].get(name, None)

        if(currentIndex is 0):
            return None
        else:
            if(scope is "Static"):
                currentIndex = dictStack[currentIndex][0]  #set the new index to the currents static link
            else: #scope is dynamic
                currentIndex = currentIndex - 1

    #static style, find dictstack where function or elem is declared following static links
    # for elem in dictStack
    # return None


#---------- Arithmetic and Comparison Operators --------------
def add():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if ((isinstance(op1,int) or (isinstance(op1,float)) and
            ((isinstance(op2,int) or (isinstance(op2,float)))))):
                opPush(op1 + op2)
        else:
            debug("Error - Invalid Operands")
    else:
        debug("Error - Stack incorrect length")

def sub():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if ((isinstance(op1,int) or (isinstance(op1,float)) and
            ((isinstance(op2,int) or (isinstance(op2,float)))))):
                opPush(op1 - op2)
        else:
            debug("Error - Invalid Operands")
    else:
        debug("Error - Stack incorrect length")

def mul():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if ((isinstance(op1,int) or (isinstance(op1,float)) and
            ((isinstance(op2,int) or (isinstance(op2,float)))))):
                opPush(op1 * op2)
        else:
            debug("Error - Invalid Operands")
    else:
        debug("Error - Stack incorrect length")

def div():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if ((isinstance(op1,int) or (isinstance(op1,float)) and
            ((isinstance(op2,int) or (isinstance(op2,float)) and (op2 != 0))))):
                opPush(op1 / op2)
        else:
            debug("Error - Invalid Operands")
    else:
        debug("Error - Stack incorrect length")

def eq():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if (op1 == op2):
            opPush(True)
        else:
            opPush(False)
    else:
        debug("Error - Stack incorrect length")

def lt():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if ((isinstance(op1,int) or (isinstance(op1,float)) and
            ((isinstance(op2,int) or (isinstance(op2,float)))))):
            if (op1 < op2):
                opPush(True)
            else:
                opPush(False)
        else:
            debug("Error: Invalid Operands")
    else:
        debug("Error - Stack incorrect length")

def gt():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if ((isinstance(op1,int) or (isinstance(op1,float)) and
            ((isinstance(op2,int) or (isinstance(op2,float)))))):
            if (op1 > op2):
                opPush(True)
            else:
                opPush(False)
        else:
            debug("Error: Invalid Operands")
    else:
        debug("Error - Stack incorrect length")

# ---------- String Operators --------------
def length():
    if (len(opStack) > 0):
        string = opPop()
        if (isinstance(string, str)):
            opPush(len(string) - 2)
        else:
            debug("Error: Invalid String Operand")
    else:
        debug("Error - Stack incorrect length")

def get():
    if (len(opStack) > 1):
        index = opPop()
        string = opPop()
        if (index > (len(string) - 1)):
            debug("Error: String index out of bounds")
            return
        if ((isinstance(string, str)) and ((isinstance(index, int)))):
            opPush(string[index])
        else:
            debug("Error: Invalid String or Index Operand")
    else:
        debug("Error - Stack incorrect length")

def getinterval():
    if (len(opStack) > 2):
        count = opPop()
        index = opPop()
        string = opPop()
        if (index > (len(string) - 1) or count > (len(string) - 1)):
            debug("Error: String index or count out of bounds")
            return
        if ((index + count) > len(string)):
            debug("Error: Counter out of range of string - cannot create substring with given length")
            return
        if ((isinstance(string, str)) and ((isinstance(index, int))) and (isinstance(count, int))):
            substring = string[index+1:((index+1) + count)]

            opPush('('+substring+')')
        else:
            debug("Error: Invalid String or Index Operand")
    else:
        debug("Error - Stack incorrect length")
# ---------- Boolean Operators --------------
def psAnd():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if (((isinstance(op1,int) or (isinstance(op1,float)) and
            (isinstance(op2, int) or (isinstance(op2, float))))) or
            (isinstance(op1, bool) and isinstance(op2, bool))):
            if (op1 == op2):
                opPush(True)
            else:
                opPush(False)
        else:
            debug("Error: Type error")
    else:
        debug("Error - Stack incorrect length")

def psOr():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        if (((isinstance(op1, int) or (isinstance(op1, float)) and
            (isinstance(op2, int) or (isinstance(op2, float))))) or
                (isinstance(op1, bool) and isinstance(op2, bool))):
            if (((op1 == True or op1 > 0) or (op2 == True or op2 > 0))):
                opPush(True)
            else:
                opPush(False)
        else:
            debug("Error: Type error")
    else:
        debug("Error - Stack incorrect length")

def psNot():
    if (len(opStack) > 0):
        op1 = opPop()
        if isinstance(op1, bool) or isinstance(op1, int):
            if isinstance(op1, bool):
                opPush(not op1)
            else:
                opPush(op1 - (2 * op1))
        else:
            debug("Error: Type error, ints and bools only")
    else:
        debug("Error - Stack incorrect length")

# ---------- Stack Manipulation and Print Operators --------------
def dup():
    if (len(opStack) > 0):
        op1 = opPop()
        opPush(op1)
        opPush(op1)
    else:
        debug("Error - Stack incorrect length")

def exch():
    if (len(opStack) > 1):
        op2 = opPop()
        op1 = opPop()
        opPush(op2)
        opPush(op1)
    else:
        debug("Error - Stack incorrect length")

def pop():
    if (len(opStack) > 0):
        op1 = opPop()
    else:
        debug("Error - Stack incorrect length")

def roll():
    if len(opStack) > 1:
        n = opPop()
        m = opPop()
        #if n is postitive
        #right rotate
        copyList = opStack[len(opStack) - m:]
        if n > 0:
            temp = copyList[n:]
            copyList[n:] = []
            copyList[:0] = temp
        elif n < 0:
            temp = copyList[0:(-1 * n)]
            copyList[: (-1 * n)] = []
            copyList[len(copyList):] = temp
        else:
            debug("Error: roll - n = 0")

        for i in range(0,m):
            pop()

        for x in copyList:
            opPush(x)
    #
    #         tempStack = (opStack[n:] + opStack[:n])
    #         clear()
    #         for i in tempStack:
    #             opStack[i] = tempStack[i]
    #     #if n is negative
    #     #left rotate
    #     if n < 0:
    #         tempStack = opStack[n:] + opStack[:n]
    #         clear()
    #         for i in tempStack:
    #             opStack[i] = tempStack[i]
    # else:
    #     debug("Error: roll - n = 0")
    #
    #   #first idea
    #    # if n > 0:
    #     #    copyList[:0] = copyList[m-n:]
    #      #   copyList[m - n:] = []
    #    # elif n < 0:
    #
    #     #else:
    #      #   debug("Error: n = 0")

def copy():
    if (len(opStack) > 0):
        opList = []                 # create copy list
        for opIndex in opStack:                 #copy current stack list into temp list
            opList[opIndex] = opStack[opIndex]
        for opIndex2 in opList:                    #push copied list on top of original stack creating copy stack
            opPush(opList[opIndex2])
    else:
        debug("Error - Stack already empty")

def clear():
    if (len(opStack) > 0):
        while len(opStack) != 0:
            opPop()
    else:
        debug("Error - Stack already empty")

def stack():
    print("==============")
    if (len(opStack) > 0):
        # stacklist = reversed(opStack)
        for i in range(len(opStack)):
            print(opStack[-(i+1)])
        print("==============")

    dictStackIndex = len(dictStack) - 1
    while(dictStackIndex != -1):
        m = dictStackIndex
        n = dictStack[dictStackIndex][0]

        print("-----" + str(m) + "-----" + str(n) + "-----")
        for i in dictStack[dictStackIndex][1]:
            print(i + "    " + str(dictStack[dictStackIndex][1].get(i)))
        dictStackIndex = dictStackIndex - 1

    print("==============")

# ---------- Dictionary Manipulation Operators --------------
def psDict():
    if len(opStack) > 0:
        opPop()
        opPush({})
    else:
        debug("Error: psDict - not enough arguments")
def begin():
    if len(opStack) > 0:
        dictPush()
    else:
        debug("Error: begin - not enough arguments")
def end():
    if len(dictStack) > 0:
        dictPop()
    else:
        debug("Error: end - not enough dictionaries to pop")
def psDef():
    if len(opStack) > 1:
        value = opPop()
        name = opPop()
        if isinstance(name, str):
            define(name, value)
        else:
            debug("Error: psDef - invalid name argument")
    else:
        debug("Error: psDef - not enough arguments")

# ---------- TEST FUNCTIONS --------------
# def testOpPop():
#     opPush(1)
#     opPush(1)
#     opPop()
#     opPop()
#     if len(opStack) != 0:
#         clear()
#         return False
#     elif len(opStack) == 0:
#         clear()
#         return True
#
# def testOpPush():
#     opPush(1)
#     opPush(98)
#     if len(opStack) == 2 and opStack[1] == 98:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testDictPop():
#     #opPush('{}')
#     #begin()
#     opPush('/y')
#     opPush(5)
#     psDef()
#     dictPop()
#     if len(dictStack) == 0:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testDictPush():
#     dictPush()
#     dictPush()
#     dictPush()
#     if len(dictStack) == 3:
#         dictPop()
#         dictPop()
#         dictPop()
#         return True
#     else:
#         dictPop()
#         dictPop()
#         dictPop()
#         return False
#
# def testDefine():
#     nam = '/testName'
#     val = 45
#
#     define(nam, val)
#     if dictStack[0][nam] == 45:         #needs work
#         clear()
#         dictPop()
#         return True
#     else:
#         clear()
#         dictPop()
#         return False
#
# def testLookup():
#     opPush('/y')
#     opPush(3)
#     psDef()
#     if lookup('y') != 3:
#         dictPop()
#         clear()
#         return False
#     elif lookup('y') == 3:
#         dictPop()
#         clear()
#         return True
#
# def testAdd():
#     opPush(1)
#     opPush(2)
#     add()
#     if opPop() != 3:
#         clear()
#         return False
#     else:
#         clear()
#         return True
#
# def testSub():
#     opPush(2)
#     opPush(2)
#     sub()
#     if opPop() != 0:
#         clear()
#         return False
#     else:
#         clear()
#         return True
#
# def testMul():
#     opPush(1)
#     opPush(2)
#     mul()
#     if opPop() != 2:
#         clear()
#         return False
#     else:
#         clear()
#         return True
#
# def testDiv():
#     opPush(4)
#     opPush(2)
#     div()
#     if opPop() != 2:
#         clear()
#         return False
#     else:
#         clear()
#         return True
#
# def testEq():
#     opPush("hi")
#     opPush("hi")        #also works with ints
#     eq()
#     if opPop() == True:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testLt():
#     opPush(1)
#     opPush(85)
#     lt()
#     if opPop() == True:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testGt():
#     opPush(56)
#     opPush(32)
#     gt()
#     if opPop() == True:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testLength():
#     opPush("Hello World")            #len of string
#     length()
#     lengthofString = opPop()
#     if(len("Hello World") == lengthofString):
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testGet():
#     opPush("Hello")
#     opPush(3)
#     get()
#     valAtIndex = opPop()
#     if valAtIndex == 'l':
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testGetInterval():
#     opPush("hello world")
#     opPush(1)
#     opPush(4)
#     getinterval()
#     interval = opPop()
#     if interval == "ello":
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testPsAnd():
#     opPush(True)
#     opPush(True)
#     psAnd()
#     value = opPop()
#     if value == True:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testPsOr():
#     opPush(True)
#     opPush(False)
#     psOr()
#     value = opPop()
#     if value == True:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testPsNot():
#     opPush(True)
#     psNot()
#     value = opPop()
#     if value == False:
#         clear()
#         return True
#     else:
#         clear()
#         return False
#
# def testDup():
#     pass
# #    valueList = []
# #    opPush(1)
# #    opPush(2)
# #    dup()
# #    for i in opStack:
# #        valueList[i] = opStack[i]
# #
# #    if valueList[0] == 1 and valueList[1] == 2:
# #        clear()
# #        return True
# #    else:
# #        clear()
# #        return False
# def testExch():
#     pass
# def testPop():
#     pass
# def testRoll():
#     pass
# def testCopy():
#     pass
# def testClear():
#     pass
# def testStack():
#     pass
# def testPsDict():
#     pass
# def testBegin():
#     pass
# def testEnd():
#     pass
# def testPsDef():
#     opPush("/y")
#     opPush(3)
#     psDef()
#     if lookup("y") != 3: return False
#     return True
# ---------- MAIN FUNCTION --------------
def main_part1():
    input1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
     """

    input2 = """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n} def
    /chic {
     /n 1 def
     /egg2 { n } def
     m n
     egg1
     egg2
     stack } def
     n
     chic
     """

    input3 = """
    /x 10 def
    /A { x } def
    /C { /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def
     B
    """
    #print(interpreter(input1, "Dynamic"))
    #print(interpreter(input1, "Static"))
    #print(interpreter(input2, "Dynamic"))
    print(interpreter(input2, "Static"))
    #print(interpreter(input3, "Dynamic"))
    #print(interpreter(input3, "Static"))


    # print('\n'"Ignore the Nones above, I think it's the testing code wigging out :) All program test cases pass"'\n')
    # testCases = [('opPop', testOpPop),
    #              ('opPush', testOpPush),
    #              ('dictPop', testDictPop),
    #              ('dictPush', testDictPush),
    #              ('define', testDefine),
    #              ('lookup', testLookup),
    #              ('add', testAdd),
    #              ('sub', testSub),
    #              ('mul', testMul),
    #              ('div', testDiv),
    #              ('eq', testEq),
    #              ('lt', testLt),
    #              ('gt', testGt),
    #              ('length', testLength),
    #              ('get', testGet),
    #              ('getinterval', testGetInterval),
    #              ('psAnd', testPsAnd),
    #              ('psOr', testPsOr),
    #              ('psNot', testPsNot),
    #              ('dup', testDup),
    #              ('exch', testExch),
    #              ('pop', testPop),
    #              ('roll', testRoll),
    #              ('copy', testCopy),
    #              ('clear', testClear),
    #              ('stack', testStack),
    #              ('psDict', testPsDict),
    #              ('begin', testBegin),
    #              ('end', testEnd),
    #              ('psDef', testPsDef)]
    #
    # failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    #
    # if failedTests:
    #     return ('Some tests failed', failedTests, 'not all tests implemented')
    # else:
    #     return ('All tests OK')


if __name__ == '__main__':
    print(main_part1())