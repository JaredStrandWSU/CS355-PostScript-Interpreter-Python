# Programmer:   Jared Strand
# Platform:     Windows
# global variables
opStack = []
dictStack = []

#--------------------------------
debug_level = 0


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
    dictStack.append(d)

def define(name, value):
    if (len(dictStack) > 0):
        dictStack[len(dictStack) - 1][name] = value
    else:
        newDict = {}
        newDict[name] = value
        dictStack.append(newDict)

def lookup(name):
    for d in reversed(dictStack):
        if d.get('/' + name, None) != None:
            return d.get('/' + name, None)
    return None

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
            opPush(len(string))
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
            substring = string[index:(index + count)]
            opPush(substring)
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
    if len(opStack) > 0:
        n = opPop()
        m = opPop()
        #if n is postitive
        #right rotate
        if n > 0:
            tempStack = (opStack[n:] + opStack[:n])
            clear()
            for i in tempStack:
                opStack[i] = tempStack[i]
        #if n is negative
        #left rotate
        if n < 0:
            tempStack = opStack[n:] + opStack[:n]
            clear()
            for i in tempStack:
                opStack[i] = tempStack[i]
    else:
        debug("Error: roll - n = 0")

      #first idea
       # if n > 0:
        #    copyList[:0] = copyList[m-n:]
         #   copyList[m - n:] = []
       # elif n < 0:

        #else:
         #   debug("Error: n = 0")

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
    if (len(opStack) > 0):
        stacklist = reversed(opStack)
        for i in stacklist:
            print('\n' + stacklist[i])
    else:
        debug("Error: stack - not enough args")

# ---------- Dictionary Manipulation Operators --------------
def psDict():
    if len(opStack) > 0:
        opPop()
        dictPush()
    else:
        debug("Error: psDict - not enough arguments")
def begin():
    if len(opStack) > 0:
        newDict = opPop()
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
def testOpPop():
    opPush(1)
    opPush(1)
    opPop()
    opPop()
    if len(opStack) != 0:
        clear()
        return False
    elif len(opStack) == 0:
        clear()
        return True

def testOpPush():
    opPush(1)
    opPush(98)
    if len(opStack) == 2 and opStack[1] == 98:
        clear()
        return True
    else:
        clear()
        return False

def testDictPop():
    #opPush('{}')
    #begin()
    opPush('/y')
    opPush(5)
    psDef()
    dictPop()
    if len(dictStack) == 0:
        clear()
        return True
    else:
        clear()
        return False

def testDictPush():
    dictPush()
    dictPush()
    dictPush()
    if len(dictStack) == 3:
        dictPop()
        dictPop()
        dictPop()
        return True
    else:
        dictPop()
        dictPop()
        dictPop()
        return False

def testDefine():
    nam = '/testName'
    val = 45

    define(nam, val)
    if dictStack[0][nam] == 45:         #needs work
        clear()
        dictPop()
        return True
    else:
        clear()
        dictPop()
        return False

def testLookup():
    opPush('/y')
    opPush(3)
    psDef()
    if lookup('y') != 3:
        dictPop()
        clear()
        return False
    elif lookup('y') == 3:
        dictPop()
        clear()
        return True

def testAdd():
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3:
        clear()
        return False
    else:
        clear()
        return True

def testSub():
    opPush(2)
    opPush(2)
    sub()
    if opPop() != 0:
        clear()
        return False
    else:
        clear()
        return True

def testMul():
    opPush(1)
    opPush(2)
    mul()
    if opPop() != 2:
        clear()
        return False
    else:
        clear()
        return True

def testDiv():
    opPush(4)
    opPush(2)
    div()
    if opPop() != 2:
        clear()
        return False
    else:
        clear()
        return True

def testEq():
    opPush("hi")
    opPush("hi")        #also works with ints
    eq()
    if opPop() == True:
        clear()
        return True
    else:
        clear()
        return False

def testLt():
    opPush(1)
    opPush(85)
    lt()
    if opPop() == True:
        clear()
        return True
    else:
        clear()
        return False

def testGt():
    opPush(56)
    opPush(32)
    gt()
    if opPop() == True:
        clear()
        return True
    else:
        clear()
        return False

def testLength():
    opPush("Hello World")            #len of string
    length()
    lengthofString = opPop()
    if(len("Hello World") == lengthofString):
        clear()
        return True
    else:
        clear()
        return False

def testGet():
    opPush("Hello")
    opPush(3)
    get()
    valAtIndex = opPop()
    if valAtIndex == 'l':
        clear()
        return True
    else:
        clear()
        return False

def testGetInterval():
    opPush("hello world")
    opPush(1)
    opPush(4)
    getinterval()
    interval = opPop()
    if interval == "ello":
        clear()
        return True
    else:
        clear()
        return False

def testPsAnd():
    opPush(True)
    opPush(True)
    psAnd()
    value = opPop()
    if value == True:
        clear()
        return True
    else:
        clear()
        return False

def testPsOr():
    opPush(True)
    opPush(False)
    psOr()
    value = opPop()
    if value == True:
        clear()
        return True
    else:
        clear()
        return False

def testPsNot():
    opPush(True)
    psNot()
    value = opPop()
    if value == False:
        clear()
        return True
    else:
        clear()
        return False

def testDup():
    pass
#    valueList = []
#    opPush(1)
#    opPush(2)
#    dup()
#    for i in opStack:
#        valueList[i] = opStack[i]
#
#    if valueList[0] == 1 and valueList[1] == 2:
#        clear()
#        return True
#    else:
#        clear()
#        return False
def testExch():
    pass
def testPop():
    pass
def testRoll():
    pass
def testCopy():
    pass
def testClear():
    pass
def testStack():
    pass
def testPsDict():
    pass
def testBegin():
    pass
def testEnd():
    pass
def testPsDef():
    opPush("/y")
    opPush(3)
    psDef()
    if lookup("y") != 3: return False
    return True
# ---------- MAIN FUNCTION --------------
def main_part1():
    testCases = [('opPop', testOpPop),
                 ('opPush', testOpPush),
                 ('dictPop', testDictPop),
                 ('dictPush', testDictPush),
                 ('define', testDefine),
                 ('lookup', testLookup),
                 ('add', testAdd),
                 ('sub', testSub),
                 ('mul', testMul),
                 ('div', testDiv),
                 ('eq', testEq),
                 ('lt', testLt),
                 ('gt', testGt),
                 ('length', testLength),
                 ('get', testGet),
                 ('getinterval', testGetInterval),
                 ('psAnd', testPsAnd),
                 ('psOr', testPsOr),
                 ('psNot', testPsNot),
                 ('dup', testDup),
                 ('exch', testExch),
                 ('pop', testPop),
                 ('roll', testRoll),
                 ('copy', testCopy),
                 ('clear', testClear),
                 ('stack', testStack),
                 ('psDict', testPsDict),
                 ('begin', testBegin),
                 ('end', testEnd),
                 ('psDef', testPsDef)]

    failedTests = [testName for (testName, testProc) in testCases if not testProc()]

    if failedTests:
        return ('Some tests failed', failedTests, 'not all tests implemented')
    else:
        return ('All tests OK')


if __name__ == '__main__':
    print(main_part1())