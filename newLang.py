from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "~"
    return data


def lex(filecontents):
    tok = ""
    state = 0
    varStarted = 0
    expr = ""
    string = ""
    var = ""
    isexpr = 0
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if char == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "~":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
                isexpr = 0
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            tok = ""
        elif tok == "\t":
            tok = ""
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            elif tokens[-1] == "LESS":
                tokens[-1] = "LESSOREQ"
            elif tokens[-1] == "GREATER":
                tokens[-1] = "GREATEROREQ"
            else:
                tokens.append("EQUALS")
            tok = ""
        elif tok == "!=" or tok == ">" or tok == "<" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            if tok == "!=":
                tokens.append("NOTEQ")
            elif tok == "<":
                tokens.append("LESS")
            elif tok == ">":
                tokens.append("GREATER")
            tok = ""
        elif tok == "$" and state == 0:
            varStarted = 1
            var += tok
            tok = ""
        elif varStarted == 1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    varStarted = 0
            var += tok
            tok = ""
        elif tok == "PRINT" or tok == "print":
            tokens.append("PRINT")
            tok = ""
        elif tok == "}":
            tokens.append("END")
            tok = ""
        elif tok == "IF" or tok == "if":
            tokens.append("IF")
            tok = ""
        elif tok == "WHILE" or tok == "while":
            tokens.append("WHILE")
            tok = ""
        elif tok == "{":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tokens.append("THEN")
            tok = ""
        elif tok == "INPUT" or tok == "input":
            tokens.append("INPUT")
            tok = ""
        elif tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9" or tok == "0":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "%" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
            elif state == 0:
                state = 1
        elif state == 1:
            string += tok
            tok = ""


    print(tokens)
    #return ''
    return tokens


def evalExpression(expr):
    return eval(expr)

    
    # Custom Evaluator:
    # i = len(expr) - 1
    # num = ""
    # print(expr)
    # while i >= 0:
    #     if expr[i] == "+" or expr[i] == "-" or expr[i] == "*" or expr[i] == "/" or expr[i] == "%":
    #         num = num[::-1]
    #         num_stack.append(num)
    #         num = ""
    #         num_stack.append(expr[i])
    #     else:
    #         num += expr[i]
    #         #The end of the expression
    #         if i == 0:
    #             num = num[::-1]
    #             num_stack.append(num)
    #     i -= 1
    # print(num_stack)
    # return "Got it"

def getVariable(var):
    if str(var[4:]) in symbols:
        return symbols[var[4:]]
    else:
        exit("Variable " + str(var[4:]) + " not defined")


def getVariableValue(var):
    if str(var[4:]) in symbols:
        if symbols[var[4:]][:3] == "NUM":
            return symbols[var[4:]][4:]
        elif symbols[var[4:]][:3] == "STR":
            if symbols[var[4:]][4] == "\"" and symbols[var[4:]][-1] == "\"":
                return symbols[var[4:]][5:-1]
            else:
                return symbols[var[4:]][4:]
            
            
    else:
        exit("Variable " + str(var[4:]) + " not defined")

def doPrint(tok1, tok2):
    if tok1 + " " + tok2[0:6] == "PRINT STRING":
        print(tok2[8:-1])
    elif tok1 + " " + tok2[0:3] == "PRINT NUM":
        print(tok2[4:])
    elif tok1 + " " + tok2[0:4] == "PRINT EXPR":
        print(evalExpression(tok2[5:]))
    elif tok1 + " " + tok2[0:3] == "PRINT VAR":
        print(getVariableValue(tok2))
        # if str(tok2[4:]) in symbols:
        #     if symbols[tok2[4:7]][:3] == "NUM":
        #         print(symbols[tok2[4:]][4:])
        #     elif symbols[tok2[4:7]][:3] == "STR":
        #         print(symbols[tok2[4:]][5:-1])

def doEvaluation(var1, operator, var2):
    if var1[:3] == "VAR":
        if var1[4:] in symbols:
            print(var1[4:])
            var1 = symbols[var1[4:]]
        else:
            exit("Variable " + str(var1[4:]) + " not defined")
    if var2[:3] == "VAR":
        if var2[4:] in symbols:
            var2 = symbols[var2[4:]]
        else:
            exit("Variable " + str(var2[4:]) + " not defined")
    if operator == "EQEQ":
        if var1 == var2:
            return True
        else:
            return False
    elif operator == "NOTEQ":
        if var1 != var2:
            return True
        else:
            return False
    #LESS THAN
    elif operator == "LESS":
        if var1[:3] == "NUM" and var2[:3] == "NUM":
            if var1[4:] < var2[4:]:
                return True
            else:
                return False
        elif var1[:3] == "STR" and var2[:3] == "STR":
            if len(var1) < len(var2):
                return True
            else:
                return False
    elif operator == "GREATER":
        if var1[:3] == "NUM" and var2[:3] == "NUM":
            if var1[4:] > var2[4:]:
                return True
            else:
                return False
        elif var1[:3] == "STR" and var2[:3] == "STR":
            if len(var1) > len(var2):
                return True
            else:
                return False
        else:
            exit("Invalid Comparison")
    elif operator == "GREATEROREQ":
        if var1[:3] == "NUM" and var2[:3] == "NUM":
            if var1[4:] >= var2[4:]:
                return True
            else:
                return False
        elif var1[:3] == "STR" and var2[:3] == "STR":
            if len(var1) >= len(var2):
                return True
            else:
                return False
        else:
            exit("Invalid Comparison")
    elif operator == "LESSOREQ":
        if var1[:3] == "NUM" and var2[:3] == "NUM":
            if var1[4:] < var2[4:]:
                return True
            else:
                return False
        elif var1[:3] == "STR" and var2[:3] == "STR":
            if len(var1) < len(var2):
                return True
            else:
                return False
        else:
            exit("Invalid Comparison")


def doInput(prompt, var):
    i = input(prompt + "\n")
    symbols[var] = "STR:" + i


def parse(tokens):
    x = 0
    execute = 1
    nestedCounter = 0
    print(tokens)
    while x < len(tokens):
        #print(x)
        if execute == 1:
            if tokens[x] == "PRINT":
                doPrint(tokens[x], tokens[x + 1]) 		
                x += 2
            elif tokens[x] == "INPUT":
                doInput(tokens[x + 1][7:], tokens[x + 2][4:])
                x += 3
            elif tokens[x][:3] == "VAR":
                if tokens[x + 1] == "EQUALS":
                    if tokens[x + 2][:3] == "NUM":
                        symbols[tokens[x][4:]] = "NUM:" + str(tokens[x + 2][4:])
                    elif tokens[x + 2][:6] == "STRING":
                        symbols[tokens[x][4:]] = "STR:" + str(tokens[x + 2][7:])
                    elif tokens[x + 2][:4] == "EXPR":
                        symbols[tokens[x][4:]] = "NUM:" + str(evalExpression(tokens[x + 2][5:]))
                    elif tokens[x + 2][:3] == "VAR":
                        symbols[tokens[x][4:]] = getVariable(tokens[x + 2])
                x += 3
            elif tokens[x] == "IF":

                if (doEvaluation(tokens[x + 1], tokens[x + 2], tokens[x + 3])):
                    execute = 1
                else:
                    execute = 0
                x += 4
            elif tokens[x] == "THEN" or tokens[x] == "END":
                if tokens[x] == "THEN":
                    nestedCounter += 1
                elif tokens[x] == "END":
                    nestedCounter -= 1
                x += 1
            elif tokens[x] == "WHILE":
                if (doEvaluation(tokens[x + 1], tokens[x + 2], tokens[x + 3])):
                    tokensInWhile = []
                    loop = True
                    counter = x + 4
                    while loop:
                        if tokens[counter] != "THEN" and tokens[counter] != "END":
                            tokensInWhile.append(tokens[counter])
                        else:
                            if tokens[counter] == "THEN":
                                print("{ FOUND")
                            elif tokens[counter] == "END":
                                print("} FOUND")
                                loop = False
                        counter += 1

                    print(tokensInWhile)
                    while doEvaluation(tokens[x + 1], tokens[x + 2], tokens[x + 3]):
                        print("")
                        parse(tokensInWhile)
                    exit()
                else:
                    execute = 0

        else:
            if tokens[x] == "END":
                if nestedCounter == 0:
                    execute = 1
            x += 1
            


    print(symbols)


def run():
    data = open_file(argv[1])
    tokens = lex(data)
    parse(tokens)



run()