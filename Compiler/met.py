# - *- coding: utf- 8 - *-
# MPOZ NTOYRAN || ALEXANDROPOULOS DIMITRIOS
# 2310         || 2928
# cs122310     || cse52928

import io
import sys

linecounter = 1
keywords = ["program", "endprogram", "decleretions", "declare", "if", "then", "else", "endif", "input", "dowhile", "while", "endwhile", "enddowhile", "loopforever", "endloop", "exit",
            "forcase", "endforcase", "incase", "endincase", "when", "endwhen", "default", "enddefault", "function", "endfunction", "return", "in", "loop", "inout", "inandout", "and", "or", "print", "not"]
lexTK = ""
quadsid = 0
listOfTemps = []
numofTMP = 0
listofQuads = []
counterforExit = 0
functionsList = []
functionL = {}
mainprogramsname = ""
inFunction=False
listOFExit = []
variableforSeeReturnCheck =""
listofFuncPars = []
argumentuniqeID = 0
entityuniquqeID = 0
nesting = 1
scopeList = [""]
afterdeletscope=[]
curnetscope = 0
def lex():
    global linecounter
    FullToken = []
    token = file.read(1)
    while 1:
        if token == " " or  token =='\t' or token == '':
            token = file.read(1)
        else:
            break

    if token.isalpha():
        FullToken.append(token)
        token = file.read(1)
        while token.isalpha() or token.isdigit():
            FullToken.append(token)
            token = file.read(1)
        # kanei ena vhma pisw se periptosh pou diavasoumai kati pou den 8eloumai
        file.seek(file.tell()-1)
        token_to_return = ''.join(FullToken)
        return token_to_return.strip()
    elif token.isdigit():
        FullToken.append(token)
        token = file.read(1)
        while token.isdigit():
            FullToken.append(token)
            token = file.read(1)
        file.seek(file.tell()-1)
        token_to_return = ''.join(FullToken)
        if int(token_to_return) < (32767 * -1) or int(token_to_return) > 32767:
            print("Number", token_to_return,"is out of bound")
            sys.exit() ##dior8osh gia ta oria ton akairaiwn
        return token_to_return.strip()
    elif token == "+":
        token_to_return = "+"
        return token_to_return.strip()
    elif token == "-":
        token_to_return = "-"
        return token_to_return.strip()
    elif token == "*":
        token = file.read(1)
        if token == "/":
            token_to_return = "*/"
            return token_to_return.strip()
        else:
            file.seek(file.tell()-1)
            token_to_return = "*"
            return token_to_return.strip()
    elif token == "/":
        token = file.read(1)
        if token == "*":
            token_to_return = "/*"
            token_to_return = skip_comment_(token_to_return)
            return token_to_return.strip()
        elif token == "/":
            token_to_return = "//"
            token_to_return = skip_comment_(token_to_return)
            return token_to_return.strip()
        else:
            file.seek(file.tell()-1)
            token_to_return = "/"
            return token_to_return.strip()
    elif token == "<":
        token = file.read(1)
        if token == ">":
            token_to_return = "<>"
            return token_to_return.strip()
        elif token == "=":
            token_to_return = "<="
            return token_to_return.strip()
        else:
            file.seek(file.tell()-1)
            token_to_return = "<"
            return token_to_return.strip()
    elif token == ">":
        token = file.read(1)
        if token == "<":
            token_to_return = "<>"
            return token_to_return.strip()
        elif token == "=":
            token_to_return = ">="
            return token_to_return.strip()
        else:
            file.seek(file.tell()-1)
            token_to_return = ">"
            return token_to_return.strip()
    elif token == "=":
        token_to_return = "="
        return token_to_return.strip()
    elif token == ":":
        token = file.read(1)
        if token == "=":
            token_to_return = ":="
            return token_to_return.strip()
        else:
            token_to_return = ":"
            file.seek(file.tell()-1)
            return token_to_return.strip()
    elif token == ";":
        token_to_return = ";"
        return token_to_return.strip()
    elif token == ",":
        token_to_return = ","
        return token_to_return.strip()
    elif token == "(":
        token_to_return = "("
        return token_to_return.strip()
    elif token == ")":
        token_to_return = ")"
        return token_to_return.strip()
    elif token == "[":
        token_to_return = "["
        return token_to_return.strip()
    elif token == "]":
        token_to_return = "]"
        return token_to_return.strip()
    elif token == "\n":
        linecounter = linecounter+1
        return "eof"
    else:
        return ("Unkown error", linecounter)
        sys.exit()

# KANEI SKIP TO COMMENT MESA APO TH LEX


def skip_comment_(tokentoretun):
    tempTK = tokentoretun

    while 1:

        if tokentoretun == "eof" or tokentoretun == "*/":
            break
        else:
            tokentoretun = lex()

    if tokentoretun == "*/" and tempTK == "/*":
        tokentoretun = lex()
        if tokentoretun == "/*" or tokentoretun == "//":
            skip_comment_(tokentoretun)
        return tokentoretun
    elif tokentoretun == "eof" and tempTK == "//":
        return tokentoretun
    else:
        print("Error in comment in line ", linecounter)
        sys.exit()


def syntaktikos_analyths():

    if 1 == program_():
        block()

# KANEI SKIP STHN EPOMENH GRAMMH

def skip_eof_():
    global linecounter
    global lexTK

    lexTK = lex()
    if lexTK == "eof":
        skip_eof_()
    else:
        pass

def program_():
    global linecounter
    global lexTK,mainprogramsname,nesting,scopeList

    skip_eof_()
    if lexTK == "program":
        lexTK = lex()
        mainprogramsname = lexTK
        scope=Scope(nesting)
        ent=Entity('-main','main',8) ##????
        scope.addentity(ent)
        scopeList[curnetscope]=scope
        if lexTK not in keywords:
            skip_eof_()

            block(mainprogramsname)
            if lexTK == "eof":
                skip_eof_()
            if lexTK == "endprogram":
                genquad("halt", "_", "_", "_")
                genquad("end_block", mainprogramsname, "_", "_")
                afterdeletscope.append(scopeList.pop(0))
        else:
            pass
    else:
        print("Error ocured 'programm' was expected in line", linecounter)
        sys.exit()

def block(funcorproName):
    global lexTK,inFunction,scopeList
    decleretions()
    subprograms()
    if funcorproName==mainprogramsname:
        inFunction=False
        genquad("begin_block", mainprogramsname, "_", "_")
    else:
        scope=scopeList[0]
        entL=scope.returnListOfEntitys()
        ent=entL[0]
        ent.setstartQuad(nextquad())
        entL[0]=ent
        scope.setListOfEntitys(entL)
        genquad("begin_block",funcorproName,"_","_")


    statments()

def decleretions():
    global linecounter
    global lexTK
    if lexTK == "declare":
        varlist()
    else:
        pass

def varlist():
    global linecounter
    global lexTK,curnetscope,scopeList

    lexTK = lex()
    serSerTemp = Entity('', '', 0)
    serSerTemp = searchScope(lexTK)
    if lexTK not in keywords and "Fail" == serSerTemp.name:
        scope=scopeList[curnetscope]
        totalscope=scope.getTotalOffset()
        ent=Entity(lexTK,"var",(totalscope+4))


        scope.addentity(ent)
        scopeList[curnetscope] = scope

        lexTK = lex()
        if lexTK == ",":
            varlist()
            pass
        elif lexTK == ";":
            skip_eof_()
            if lexTK=="declare": #dior8osh gia thn periptosh pou exoumai 2 synexomenes declare
                varlist()
            pass
        else:
            print("Variable decleretion error in line ", linecounter)
            sys.exit()
    else:
        print("Declared variable is a keyword in line or was already declered:", linecounter, lexTK)
        sys.exit()

def subprograms():

    while lexTK == "function":
        subprogram()

def subprogram():
    global linecounter
    global lexTK
    global functionsList,variableforSeeReturnCheck,functionL,nesting,curnetscope,afterdeletscope
    if lexTK == "function":
        lexTK = lex()
        nesting=nesting+1
        if lexTK in functionL:
            print("Error function with same name already exist NAME ",lexTK)
            sys.exit()
        functionsList.append(lexTK)
        functionL.update({lexTK:0})
        variableforSeeReturnCheck=lexTK
        serSerTemp = Entity('', '', 0)
        serSerTemp = searchScope(lexTK)
        if lexTK in keywords or lexTK == serSerTemp.name:
            print(
                "The name of the function is a keyword or variable error ocured in line:", linecounter)
            sys.exit()
        else:
            subproname=lexTK
            scope=Scope(nesting)
            ent=Entity(subproname,"function",8)
            scope.addentity(ent)
            scopeList.insert(0,scope)

            funcbody(lexTK)
            if lexTK == "eof":
                skip_eof_()
            if lexTK == "endfunction":
                scopePrevious=scopeList[curnetscope+1]
                scope=scopeList[curnetscope]
                enL=scope.returnListOfEntitys()
                ent=enL[0]
                entemp=enL[-1]
                ent.changeoffset(scopePrevious.getTotalOffset())
                ent.setframelength(entemp.returnoffset())
                scopePrevious.addentity(ent)
                genquad("end_block", subproname, "_", "_")
                nesting=nesting-1
                afterdeletscope.append(scopeList.pop(0))
                skip_eof_()
            else:
                print("The function have no end error ocured in line ", linecounter,lexTK)
                sys.exit()
    else:
        pass

    variableforSeeReturnCheck=functionsList.pop(0)

def funcbody(subproName):
    global inFunction
    inFunction=True
    formalpars()
    block(subproName)

def formalpars():
    global linecounter
    global lexTK

    lexTK = lex()
    if lexTK == "(":
        formalparlist()
        if lexTK == ")":
            skip_eof_()
            pass
        else:
            print("Error ocured ) expected in line ", linecounter)
            sys.exit()
    else:
        print(
            "Error ocured aafter ( was expected after function declaration in line ", linecounter)
        sys.exit()

def formalparlist():
    global linecounter
    global lexTK

    if lexTK == ")":
        pass
    else:
        formalparitem()

def formalparitem():

    global linecounter
    global lexTK,listofFuncPars,scopeList
    lexTK = lex()
    scope=scopeList[curnetscope]
    if lexTK == "in":
        lexTK = lex()
        if lexTK not in keywords:
            ent=Entity(lexTK,"var",(scope.getTotalOffset()+4))
            ent.setParMode("in")
            scope.addentity(ent)
            arg=Argument("in","int")
            entL=scope.returnListOfEntitys() ##pernei th lista me ta entitys apo to scope
            ent=entL[0] #pernei to teleutaio entity pou einai to entity ths functio
            ent.setArgument(arg)#vazei to arg sto entity
            entL[0]=ent # antika8ista sthn teleutaia 8esh ths listas me ta entity to entity
            scope.setListOfEntitys(entL)
            scopeList[curnetscope]=scope
            lexTK = lex()
            if lexTK == ",":
                formalparitem()
            else:
                pass
        else:
            print("Error ocured invalid variable after in ", linecounter)
            sys.exit()
    elif lexTK == "inout":
        lexTK = lex()
        if lexTK not in keywords:
            ent=Entity(lexTK,"var",(scope.getTotalOffset()+4))
            ent.setParMode("inout")
            scope.addentity(ent)
            arg=Argument("inout","int")
            entL=scope.returnListOfEntitys() ##pernei th lista me ta entitys apo to scope
            ent=entL[0] #pernei to teleutaio entity pou einai to entity ths functio
            ent.setArgument(arg)#vazei to arg sto entity
            entL[0]=ent # antika8ista sthn teleutaia 8esh ths listas me ta entity to entity
            scope.setListOfEntitys(entL)
            scopeList[curnetscope]=scope
            lexTK = lex()
            if lexTK == ",":
                formalparitem()
            else:
                pass
        else:
            print("Error ocured invalid variable after inout ", linecounter)
            sys.exit()
    elif lexTK == "inandout":
        lexTK = lex()
        if lexTK not in keywords:
            ent=Entity(lexTK,"var",(scope.getTotalOffset()+4))
            ent.setParMode("inandout")
            scope.addentity(ent)
            arg=Argument("inandout","int")
            entL=scope.returnListOfEntitys() ##pernei th lista me ta entitys apo to scope
            ent=entL[0] #pernei to teleutaio entity pou einai to entity ths functio
            ent.setArgument(arg)#vazei to arg sto entity
            entL[0]=ent # antika8ista sthn teleutaia 8esh ths listas me ta entity to entity
            scope.setListOfEntitys(entL)
            scopeList[curnetscope]=scope
            lexTK = lex()
            if lexTK == ",":
                formalparitem()
            else:
                pass
        else:
            print("Error ocured invalid variable after inandout ", linecounter)
            sys.exit()
    else:
        print("Error ocured in line ", linecounter)
        sys.exit()

def statments():
    global linecounter
    global lexTK#, listofAssigment

    statment()
    while lexTK == ";":
        skip_eof_()
        statment()

def statment():
    global linecounter
    global lexTK
    if lexTK not in keywords:
        assignment_stat()
    elif lexTK == "if":
        if_stat()
    elif lexTK == "while":
        while_stat()
    elif lexTK == "dowhile":
        do_while_stat()
    elif lexTK == "loop":
        loop_stat()
    elif lexTK == "exit":
        exit_stat()
    elif lexTK == "forcase":
        forcase_stat()
    elif lexTK == "incase":
        incase_stat()
    elif lexTK == "return":
        return_stat()
    elif lexTK == "input":
        input_stat()
    elif lexTK == "print":
        print_stat()
    else:
        pass

def assignment_stat():
    global linecounter
    global lexTK
    global assigafterif
    tempVar = searchScope(lexTK)
    if tempVar.name=='Fail':
        print('Error variable ',lexTK,' not declared in line ',linecounter)
        sys.exit()
    lexTK = lex()
    if lexTK == ":=":
        lexTK = lex()
        exp=expresion()
        if exp not in keywords:
            genquad(":=",exp,"_",tempVar.name)

    else:
        print("Error ocured after := expresion expected in line ",
              linecounter,' ', lexTK)
        sys.exit()

def if_stat():
    global lexTK, linecounter,lisofAssigments

    lexTK = lex()
    if lexTK == "(":
        b_true, b_false =condition()

        if lexTK == ")":
            lexTK = lex()

            if lexTK == "then":
                skip_eof_()
                backpatch(b_true, nextquad())
                statments()
                skip_eof_()
                temp = makelist(nextquad())
                genquad('jump',"_","_","_")
                backpatch(b_false, nextquad())
                elsepart()
                backpatch(temp, nextquad())
                if lexTK == "eof":
                    skip_eof_()
                if lexTK == "endif":
                    lexTK = lex()
                else:
                    print("The if statment cant work cause it neverends", linecounter)
                    sys.exit()
        else:
            print("Error in closing if ) expected in line ",linecounter, lexTK)
            sys.exit()
    else:
        print("Error ocured ( expected after if in line ", linecounter)
        sys.exit()

def elsepart():
    global linecounter
    global lexTK

    if lexTK == "else":
        skip_eof_()
        statments()

    else:
        pass

def actualpars(nameforcall):
    global linecounter
    global keywords
    global lexTK,variableforSeeReturnCheck


    if lexTK == "(":
        actualparlist(nameforcall)
        if lexTK == ")":
            w = newtemp()
            s=scopeList[0]
            serSerTemp = Entity('', '', 0)
            serSerTemp = searchScope(w)
            if 	"Fail" == serSerTemp.name:##pi8anwn la8os apo ena tab
                ent=Entity(w,"var",s.getTotalOffset()+4)
                s.addentity(ent)
                scopeList[0]=s
            genquad("par",w, "RET","_")
            genquad("call",nameforcall,"_","_")
            skip_eof_()

        else:
            print("Error in actualpars in line  ", linecounter)
            sys.exit()
    else:
        pass

    return w

def actualparlist(nameforcall):
    global linecounter
    global keywords
    global lexTK,listofFuncPars
    x = Entity(nameforcall,"funtionForCheck",0)
    listofFuncPars.insert(0,x)
    actualparitem(nameforcall)
    while lexTK == ",":
        actualparitem(nameforcall)



def actualparitem(nameforcall):
    global linecounter
    global lexTK,listofFuncPars
    lexTK = lex()
    x=listofFuncPars[0]

    if lexTK == "in":
        lexTK = lex()
        arg=Argument("in","int")
        x.setArgument(arg)
        exp=expresion()
        genquad("par",exp,"CV","_")
    elif lexTK == "inout":
        lexTK = lex()
        arg=Argument("inout","int")
        x.setArgument(arg)
        if lexTK not in keywords:
            genquad("par",lexTK,"REF","_")
            lexTK = lex()
        else:
            print(
                "After the inout an id that is not keywords is expected in linecounter ", linecounter)
            sys.exit()
    elif lexTK == "inandout":
        lexTK = lex()
        arg=Argument("inandout","int")
        x.setArgument(arg)
        if lexTK not in keywords:
            genquad("par",lexTK,"RET","_")
            lexTK = lex()
        else:
            print(
                "After the inout an id that is not keywords is expected in linecounter ", linecounter)
            sys.exit()
    else:
        print("Error in actalparlist in line ", linecounter, lexTK)
        sys.exit()

    listofFuncPars[0]=x

def expresion():
    global linecounter
    global lexTK,scopeList,curnetscope,numofTMP
    opsig=optional_sign()
    term1=term()
    serSerTemp = searchScope(term1)
    if term1 != serSerTemp.name:
        print("Variable term", term1, "not declared in line ", linecounter)
        sys.exit()
    scope=scopeList[curnetscope]
    while lexTK == "+" or lexTK == "-":
        opsig=lexTK
        lexTK = lex()
        serSerTemp = Entity('', '', 0)
        serSerTemp = searchScope(lexTK)
        if lexTK != serSerTemp.name:
            print("Variable", lexTK,"not declared in line ",linecounter)
            sys.exit()
        term2=term()
        serSerTemp = searchScope(term2)
        if term2 != serSerTemp.name:
            print("Variable term", term2 ,"not declared in line ",linecounter)
            sys.exit()
        temp=newtemp()
        serSerTemp = searchScope(temp)
        if "Fail" == serSerTemp.name:

            scoOff=scope.getTotalOffset()
            ent=Entity(temp,"var",scoOff+4)
            scope.addentity(ent)

        genquad(opsig, term1, term2, temp)

        term1=temp
    scopeList[curnetscope]=scope
    serSerTemp = searchScope(term1)###????
    if term1 != serSerTemp.name:
        print("Variable term", term1,"not declared in line ",linecounter)
        sys.exit()


    numofTMP=0
    return term1

def term():
    global linecounter
    global keywords
    global lexTK
    global numofTMP
    fact1=factor()
    scope=scopeList[curnetscope]
    while lexTK == "*" or lexTK == "/":

        opsig=lexTK
        lexTK = lex()
        serSerTemp = Entity('', '', 0)
        serSerTemp = searchScope(lexTK)
        if lexTK != serSerTemp.name:
            print("Variable", lexTK,"not declared in line ",linecounter)
            sys.exit()
        fact2=factor()
        serSerTemp = searchScope(fact2)
        if fact2 != serSerTemp.name:
            print("Variable term", fact2,"not declared in line ",linecounter)
            sys.exit()
        temp=newtemp()
        serSerTemp = searchScope(temp)
        if "Fail" == serSerTemp.name:
            scoOff=scope.getTotalOffset()
            ent=Entity(temp,"var",scoOff+4)
            scope.addentity(ent)
        genquad(opsig, fact1, fact2, temp)
        fact1=temp

    scopeList[curnetscope]=scope
    return fact1

def factor():
    global linecounter
    global lexTK,scopeList
    scope=scopeList[curnetscope]
    if lexTK.isdigit():
        vtoreturn=lexTK
        lexTK = lex()
    elif lexTK == "(":
        vtoreturn=lexTK
        lexTK = lex()
        expresion()
        if lexTK == ")":
            pass
        else:
            print("Error with closing expresion with ) in line ", linecounter)
            sys.exit()
    elif lexTK.isalnum() and lexTK not in keywords:
        vtoreturn=lexTK
        lexTK = lex()
        vtoreturn=idtail(vtoreturn) #to v toreturn allazei edw epidi sthn periptosh call w = newTemp() par, w, RET, _ xriazomaste to w to opio einai temp kai epistrefei
    else:
        print("Error in factor", lexTK)
        sys.exit()

    return vtoreturn

def idtail(nameforcall):
    global linecounter
    global keywords
    global lexTK
    w = nameforcall

    if lexTK == "(":
        w =actualpars(nameforcall)
    else:
        pass

    return w

def optional_sign():
    global linecounter
    global keywords
    global lexTK

    if lexTK == "+" or lexTK == "-":
        add_oper()
    else:
        pass

    return lexTK

def while_stat():
    global lexTK
    global linecounter
    lexTK = lex()
    if lexTK == "(":
        WhileStar=nextquad()
        b_true,b_false = condition()
        if lexTK == ")":
            skip_eof_()
            backpatch(b_true,nextquad())
            statments()
            genquad("jump","_","_",WhileStar)
            backpatch(b_false,nextquad())
            skip_eof_()
            if lexTK == "endwhile":
                skip_eof_()
            else:
                print("While never ends in line", linecounter)
                sys.exit()
        else:
            print("Error after condition in while ) expected", linecounter)
            sys.exit()
    else:
        print("After while ( expected in line", linecounter)
        sys.exit()

def do_while_stat():
    global lexTK
    global linecounter
    doWhileStart=nextquad()
    skip_eof_()
    statments()
    skip_eof_()
    if lexTK == "enddowhile":
        lexTK = lex()
        if lexTK == "(":
            b_true,b_false = condition()
            backpatch(b_true,doWhileStart)
            backpatch(b_false,nextquad())
            if lexTK == ")":
                skip_eof_()
            else:
                print("Error ) expected after condition in linecounter ",
                      linecounter)
                sys.exit()
        else:
            print("Error ( expected after enddowhile in line counter", linecounter)
            sys.exit()
    else:
        print("Error enddowhile expected in line", linecounter)
        sys.exit()

def loop_stat():
    global listOFExit,counterforExit##me vash ayth thn lista kanei exit apo th loop me mia jump sto telos ths loop

    returnListOfEntitystoloopstart=nextquad()
    counterforExit=counterforExit+1
    skip_eof_()
    statments()
    if lexTK == "eof":
        skip_eof_()
    else:
        pass

    if lexTK == "endloop":
        skip_eof_()
        genquad("jump","_","_",returnListOfEntitystoloopstart)
        if not listOFExit:
            print("# WARNING: No exit in loop")
        else:
            backpatch(listOFExit.pop(0),nextquad())
            counterforExit=counterforExit-1
        if lexTK == ";":
            pass
        else:
            pass
    else:
        print("Loop never ends in line ", linecounter)
        sys.exit()

def exit_stat():
    global lexTK,listOFExit,counterforExit
    if lexTK == "exit":
        if counterforExit==0:
            print("Exit found out of a loop in line ",linecounter) ##ka8efwra pou mpenei se loop kanei +1 sto counterforExit molis vgenei kanei -1 se periptosh loop mesa se loop douleuei
            sys.exit()
        listOFExit.append(makelist(nextquad()))
        lexTK=lex()
        genquad("jump","_","_","_") ##8a paei sto endofloop


def forcase_stat():
    global lexTK
    skip_eof_()
    bb_true=[]
    forcasseStart=nextquad()
    while lexTK == "whene":
        lexTK = lex()
        if lexTK == "(":
            b_true,b_false=condition()
            if lexTK == ")":
                lexTK = lex()
                if lexTK == ":":
                    lexTK = lex()
                    backpatch(b_true,nextquad())##ektelei ta statments an isxuei
                    statments()
                    bb_true.append(nextquad())##gina dipou 8a kanei to jump an kapio condition isxuei kanei backpatch to bbtrue meta to telos ths end
                    genquad("jump","_","_","_")##kanei to jump an kapio condition isxuei
                    backpatch(b_false,nextquad())
                    skip_eof_()
                else:
                    print(
                        "Error ocured in forcase after condition : sign was expected in line", linecounter)
                    sys.exit()
            else:
                print(
                    "Error ocured in forcase after condition ) sign was expected in line", linecounter)
                sys.exit()
        else:
            print(
                "Error ocured in forcase after whene ( sign was expected in line", linecounter)
            sys.exit()

    if lexTK == "default":
        lexTK = lex()
        if lexTK == ":":
            lexTK = lex()
            backpatch(b_false,nextquad())
            statments()
            if lexTK == "enddefault":
                genquad("jump","_","_",forcasseStart)
                backpatch(bb_true,nextquad())
                skip_eof_()
            else:
                print("Forcase never ends error ocured in line ", linecounter)
                sys.exit()
        else:
            print("Affter default : sign was expected error ocure in line ", linecounter)
            sys.exit()
    else:
        print("Default keywords was expected in forcase in line ", linecounter)
        sys.exit()

    if lexTK == "endforcase":
        skip_eof_()
    else:
        print("Forcase never ends in line ", linecounter)
        sys.exit()

def incase_stat():
    global lexTK
    skip_eof_()
    bb_true=[]
    incaseStart=nextquad()
    while lexTK == "whene":
        lexTK = lex()
        if lexTK == "(":
            b_true,b_false = condition()
            if lexTK == ")":
                lexTK = lex()
                if lexTK == ":":
                    lexTK = lex()
                    backpatch(b_true,nextquad())
                    statments()
                    genquad("jump","_","_",incaseStart)
                    backpatch(b_false,nextquad())
                    skip_eof_()
                else:
                    print(
                        "Error ocured in incase after condition : sign was expected in line", linecounter)
                    sys.exit()
            else:
                print(
                    "Error ocured in incase after condition ) sign was expected in line", linecounter)
                sys.exit()
        else:
            print(
                "Error ocured in incase after whene ( sign was expected in line", linecounter)
            sys.exit()

    if lexTK == "endincase":
        skip_eof_()
    else:
        print("Incase never ends error ocured in line ", linecounter)
        sys.exit()

def return_stat():
    global lexTK
    global linecounter,variableforSeeReturnCheck,functionL,inFunction
    lexTK = lex()
    exp=expresion()
    genquad("retv",exp,"_","_")
    functionL[variableforSeeReturnCheck]=1
    if(inFunction==False):
        print("Return value out of function detected in line ",linecounter)
        sys.exit()

def input_stat():
    global lexTK
    lexTK = lex()
    var=searchScope(lexTK)
    if lexTK.isalnum() and lexTK not in keywords and lexTK==var.name:
        genquad("inp",lexTK,"_","_")
        skip_eof_()
    else:
        print("Error ocured after input the id is not acceptable ", linecounter)
        sys.exit()


def print_stat():
    global lexTK
    lexTK = lex()
    exp=expresion()
    genquad("out",exp,"_","_")


def condition():
    global lexTK
    global ifswitch
    b_true, b_false = Q1_true, Q1_false = boolterm()
    while lexTK == "or":
        backpatch(b_false, nextquad())
        Q2_true, Q2_false = boolterm()
        b_true = merge(b_true, Q2_true)
        b_false = Q2_false

    return b_true, b_false


def boolterm():
    global lexTK
    Q_true, Q_false = R1_true, R1_false =boolfactor()

    while lexTK == "and":
        backpatch(Q_true,nextquad())
        R2_true, R2_false = boolfactor()
        Q_false = merge(Q_false, R2_false)
        Q_true = R2_true

    return Q_true, Q_false


def boolfactor():
    global linecounter
    global keywords
    global lexTK
    #global listofAssigment
    lexTK = lex()
    if lexTK == "not":
        lexTK = lex()
        if lexTK == "[":
            b_false,b_true, = condition()
            if lexTK == "]":
                lexTK = lex()
            else:
                print("Error ] expected after the condition in line ", linecounter)
                sys.exit()
        else:
            print("Error after not expected [ in line ", linecounter)
            sys.exit()
    elif lexTK == "[":
        b_true,b_false = condition()
        if lexTK == "]":
            skip_eof_()
        else:
            print("Error ] expected after the condition in line ", linecounter)
            sys.exit()
    else:
        x=expresion()
        liscondi=emptrylist()
        reletional_oper()
        relop=lexTK
        lexTK = lex()
        y=expresion()
        b_true = makelist(nextquad())
        genquad(relop, x, y,"_")
        b_false = makelist(nextquad())
        genquad('jump',"_","_","_")

    return b_true,b_false


def reletional_oper():
    global linecounter
    global keywords
    global lexTK

    if lexTK == "=":
        pass
    elif lexTK == "<=":
        pass
    elif lexTK == ">=":
        pass
    elif lexTK == ">":
        pass
    elif lexTK == "<":
        pass
    elif lexTK == "<>":
        pass
    else:
        print("Error ocured reletional oper is wrong in line:", linecounter, lexTK)
        sys.exit()


def add_oper():
    global linecounter
    global lexTK
    if lexTK == "+":
        lexTK = lex()
    elif lexTK == "-":
        lexTK = lex()
    else:
        print("Error ocured in add oper is wrong in line:", linecounter)
        sys.exit()


def mul_oper():
    global linecounter
    global lexTK

    if lexTK == "*":
        lexTK = lex()
    elif lexTK == "/":
        lexTK = lex()

    else:
        print("Error ocured in mul oper is wrong in line:", linecounter)
        sys.exit()


class NewQuad:
    def __init__(self, quadid, operetion, variable1, variable2, variable3):
        self.quadid = int(quadid)
        self.operetion = str(operetion)
        self.variable1 = str(variable1)
        self.variable2 = str(variable2)
        self.variable3 = str(variable3)

    def myfunc(self):
        print("" + self.quadid + ":" + self.operetion + "," +
              self.variable1 + "," + self.variable2 + "," + self.variable3)

    def changeLastvar(self,var3):
        self.variable3=str(var3)

def genquad(op, x, y, z):
    global quadsid, listofQuads
    quadsid = quadsid+1
    if z in keywords:
        print("Error in genquad z cannot be anyything else than a variable")
        sys.exit()

    newquad= NewQuad(quadsid, op, x, y, z)
    listofQuads.append(newquad)

def nextquad():
    global quadsid
    return quadsid+1

def newtemp():
    t_ = 'T_'
    global listOfTemps
    global numofTMP,scopeList
    if numofTMP == 8:##gia periptosh pou to expresion einai poly megalw kai me vash oti oi temp register den einai perisoteroi apo 10 0-9
        numofTMP=0
    strnumofTMP = str(numofTMP)
    nameofTMPvar = t_+strnumofTMP
    numofTMP = numofTMP+1
    listOfTemps.append(nameofTMPvar)


    return nameofTMPvar

def emptrylist():
    newlist = list()
    return newlist

def makelist(x):
    newlist = list()
    newlist.append(x)
    return newlist

def merge(list1, list2):
    newlist =list1+list2
    return newlist

def backpatch(quadswith, nextq):
    global listofQuads
    for q in listofQuads:
        if q.quadid in quadswith:
            q.variable3 = nextq

def transform_to_c(quad):
    flag = True
    if quad.operetion == 'jump':
        ret = 'goto L_' + str(quad.variable3) + ';'
    elif quad.operetion in ('+','-','*','/'):
        ret = quad.variable3 + '=' + str(quad.variable1) + ' ' + str(quad.operetion) + ' ' + str(quad.variable2) + ';'
    elif quad.operetion in ('=', '<>', '<', '<=', '>', '>='):
        op = quad.operetion
        if op == '=':
            op = '=='
        elif op == '<>':
            op = '!='
        ret = 'if (' + str(quad.variable1) + ' ' + op + ' ' + str(quad.variable2) + ')goto L_' + str(quad.variable3) + ';'
    elif quad.operetion == ':=':
        ret = quad.variable3 + ' = ' + str(quad.variable1) + ';'
    elif quad.operetion == 'retv':
        ret = 'return (' + str(quad.variable1) + ');'
    elif quad.operetion == 'out':
        ret = 'printf("%d\\n", ' + str(quad.variable1) + ');'
    elif quad.operetion == 'begin_block':
        flag = False
        if quad.variable1 == mainprogramsname:
            ret = 'int main(void)\n{'
            sco=scopeList[-1]
        else:
            ret = 'int ' + quad.variable1 + '('
            sco=afterdeletscope.pop(0)
            scopel=sco.returnListOfEntitys()
            inp=""
            for x in scopel:
                if x.parMode != "":
                    inp=inp+"int "+ x.name+"," ##Vazei ta orismata sths synarthshs me vash to symbol table
            inp=inp[:-1] + ")\n{"
            ret = ret + inp

        declareing = "\n\tint "
        scopel=sco.returnListOfEntitys()       ##vazei ta declared mesa sthn synarthsh
        for x in scopel:
            if x.typeofEntity == "var" and x.parMode=="":
                declareing=declareing+x.name+","

        declareing=declareing[:-1]+";\n"
        ret=ret+declareing
    elif quad.operetion == 'end_block':
        flag = False
        ret="}\n"
    elif quad.operetion == 'halt':
        ret = 'return 0;'
    elif quad.operetion == 'inp':
        ret = 'scanf("%d",' + str(quad.variable1) + ');'
    else:
        ret = " ///////"

    if flag == True:
        ret = '\tL_' + str(quad.quadid) + ': ' + ret
    return ret

def gnlvcode(v):
    for x in scopeList:
        scope=x
        listforentitys = scope.returnListOfEntitys()
        for ent in listforentitys:
            if ent.name == v :
                v = ent
                i = scope.nestingLevel

    x=nesting
    gnvlcodeReturn = 'lw $t0,-4($sp)\n'
    while 1:
        gnvlcodeReturn = gnvlcodeReturn + '\t\tlw $t0, -4($s0)\n'
        x = x+1
        if x >= i:
            break


    gnvlcodeReturn = gnvlcodeReturn + '\t\tadd $t0,$t0,-' + str(v.offset) + '\n'
    return gnvlcodeReturn


def loadvar(quadvar,tempregister):
    global nesting
    i =-1
    for scope in scopeList:
        listforentitys = scope.returnListOfEntitys()
        m=listforentitys[0]
        for ent in listforentitys:
            if ent.name == quadvar and i==-1:
                v = ent
                i = scope.nestingLevel


    if quadvar.isdigit():
        loadvarReturn = 'li $t'+str(tempregister)+','+str(quadvar)+'\n'
    elif i == 1:
        loadvarReturn = 'lw $t'+str(tempregister)+',-' +str(v.offset)+'($s0)\n'
    elif v.parMode == '' and i == nesting or v.parMode == 'in' and i == nesting or quadvar[0:2] == "T_":
        loadvarReturn = 'lw $t'+str(tempregister)+',-' + str(v.offset)+'($sp)\n'
    elif  v.parMode == 'inout' and i==nesting :
        loadvarReturn = 'lw $t0,-'+str(v.offset)+'($sp)\n\t\t' + 'lw $t' + str(tempregister)+',($t0)\n'
    elif v.parMode == '' and i == nesting or v.parMode == 'in' or i < nesting:
        loadvarReturn = gnlvcode(v.name) + '\t\tlw $t'+ str(tempregister)+',($t0)\n'
    elif v.parMode == 'inout' and i < nesting:
        loadvarReturn = gnlvcode(quadvar) + '\t\tlw $t0,($t0)\n' + '\t\tlw $t'+ str(tempregister)+ ',($t0)\n'
    else:
        loadvarReturn = 'Error in loadvar\n'
        print(loadvarReturn)
    return '\t\t'+loadvarReturn

def storevar(r,v):
    i=-1
    for scope in scopeList:
        listforentitys = scope.returnListOfEntitys()
        for ent in listforentitys:
            if ent.name == v and i == -1:
                v = ent
                i = scope.nestingLevel
                break

    scope = scopeList[0]
    localVar = scope.varLocal(v.name)
    ## 8a mporousamai na xrisimopisoumai to search scope alla 8a eixamai 8ema me to nesting
    if i == 1:
        storevarReturn = 'sw $t' + str(r) + ',-' + str(v.offset) + '($s0)\n'
    elif localVar == 1 or v.name[0:2] == "T_" or v.parMode == 'in' and i == nesting:
        storevarReturn = 'sw $t' + str(r) + ',-' + str(v.offset) + '($sp)\n'
    elif v.parMode == 'inout' and i == nesting:
        storevarReturn = 'lw $t0, -' +str(v.offset) + '($sp)\n\t\t' + 'sw $t'+str(r)+',($t0)\n'
    elif v.parMode == '' and localVar == 1 or v.parMode == 'in' or i < nesting:
        storevarReturn = gnlvcode(v.name) + '\t\tsw $t' +str(r) +'($t0)'
    elif v.parMode == 'inout' and i < nesting:
        storevarReturn = gnlvcode(v.name) + '\t\tlw $t0,($t0)' + '\n\t\tsw $t' + str(r) + '($t0)\n'
    else:
        storevarReturn = 'Error in storevar'

    return '\t\t' + storevarReturn

def transform_to_finalCode(quad):
    global curnetscope,nesting,frameLengthValu,scopeList
    global quadsid ##to xrisimopioumai ghia counter gia ton ariui8mo twn parametrwn pou vazoumai
    flag = True
    num1=1
    num2=2
    num3=3
    if quad.operetion == 'jump':
        ret = '\t\tj L_' + str(quad.variable3)
    elif quad.operetion == '+':
        ret = (loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) + '\t\tadd ' + '$t' + str(num3) + ',$t' + str(num1) + ',$t' + str(num2) + '\n' +storevar(num3,quad.variable3))
    elif quad.operetion == '-':
        ret = (loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) + '\t\tsub ' + '$t' + str(num3) + ',$t' + str(num1) + ',$t' + str(num2) + '\n' +storevar(num3,quad.variable3))
    elif quad.operetion == '*':
        ret = (loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) + '\t\tmul ' + '$t' + str(num3) + ',$t' + str(num1) + ',$t' + str(num2) + '\n' +storevar(num3,quad.variable3))
    elif quad.operetion == '/':
        ret = (loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) + '\t\tdiv ' + '$t' + str(num3) + ',$t' + str(num1) + ',$t' + str(num2) + '\n' +storevar(num3,quad.variable3))
    elif quad.operetion == '=':
        ret = loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) +'\t\tbeq $t' + str(num1) + ',$t' + str(num2) + ',L_' + str(quad.variable3)
    elif quad.operetion == '<':
        ret = loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) +'\t\tblt $t' + str(num1) + ',$t' + str(num2) + ',L_' + str(quad.variable3)
    elif quad.operetion == '>':
        ret = loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) +'\t\tbgt $t' + str(num1) + ',$t' + str(num2) + ',L_' + str(quad.variable3)
    elif quad.operetion == '<=':
        ret = loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) +'\t\tble $t' + str(num1) + ',$t' + str(num2) + ',L_' + str(quad.variable3)
    elif quad.operetion == '>=':
        ret = loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) +'\t\tbge $t' + str(num1) + ',$t' + str(num2) + ',L_' + str(quad.variable3)
    elif quad.operetion == '<>':
        ret = loadvar(quad.variable1, num1) + loadvar(quad.variable2, num2) +'\t\tbne $t' + str(num1) + ',$t' + str(num2) + ',L_' + str(quad.variable3)
    elif quad.operetion == ':=':
        ret = loadvar(quad.variable1,num1) + storevar(num1,quad.variable3)
    elif quad.operetion == 'begin_block':
        flag = False
        if quad.variable1 == mainprogramsname:
            curnetscope = -1
            nesting = 1
            for scope in afterdeletscope:
                if scope.nestingLevel == 1:
                    frameLengthValu = scope.getTotalOffset()
            ret = '#---------------------------------------------\n\n'
            ret = ret + '\tLmain:\n' +'\t\tsw $ra,($sp)\n'+ "\t\t" + 'add $sp,$sp,' + str(frameLengthValu)+ '\n\t\t' + 'move $s0,$sp'
        else:
            curnetscope = 0
            for scope in afterdeletscope:
                if scope.nestingLevel > 1:
                    listofentitys=scope.returnListOfEntitys()
                    entity=listofentitys[0]
                    if entity.name == quad.variable1:
                        frameLengthValu=entity.framelength
                        nesting=scope.nestingLevel
            ret = '#---------------------------------------------\n\n'
            ret = ret + '\t' + quad.variable1 + ':' + '\n\t\t'+ 'sw $ra,($sp)' ## den einai teliomeno '\t\tadd $fp,$sp,'+ str(frameLengthValu)+
    elif quad.operetion == 'end_block':
        flag = False
        temp=scopeList.pop(0)
        temp=temp.returnListOfEntitys()
        temp=temp[0]
        ret = ''
    elif quad.operetion == 'halt':
        ret = '\t\tli $v0,10\n\t\t' + 'syscall'
    elif quad.operetion == 'inp':
        v = searchScope(quad.variable1)
        ret = '\t\tli $v0,5\n\t\t' + 'syscall\n\t\t' + '\n\t\tmove $t0,$v0\n\t\t' + storevar(0,v)
    elif quad.operetion == 'out':
        v = searchScope(quad.variable1)
        ret = '\t\tli $v0,1\n' +loadvar(v.name,0)+ '\n\t\tmove $a0,$t0' + '\n\t\t' + 'syscall'
    elif quad.operetion == 'retv':
        ret = loadvar(quad.variable1,1) + '\t\tmove $v0,$t1\n\t\tlw $ra,($sp)' + '\n\t\tjr $ra'
    elif quad.operetion == 'par' and quad.variable2 == 'CV':
        if quadsid ==0:
            for q in listofQuads:
                if q.quadid == quad.quadid:
                    num3 = -1
                elif num3 == -1 and q.operetion == 'call':
                    num3 = searchScope(q.variable1)
                    frameLength=num3.framelength
                    break

            ret = '\t\tadd $fp,$sp,' + str(frameLength) + '\n'
        else:
            ret = ''

        temp = 12+4*quadsid
        quadsid = quadsid + 1
        ret = ret + loadvar(quad.variable1,0) + '\t\tsw $t0, -'+ str(temp) +'($fp)' ##όπου i ο αύξων αριθμός της παραμέτρου
    elif quad.operetion == 'par' and quad.variable2 == 'RET':
        if quadsid ==0:
            for q in listofQuads:
                if q.quadid == quad.quadid:
                    num3 = -1
                elif num3 == -1 and q.operetion == 'call':
                    num3 = searchScope(q.variable1)
                    frameLength=num3.framelength
                    break

            ret = '\t\tadd $fp,$sp,' + str(frameLength) + '\n'
        else:
            ret = ''
        s=searchScope(quad.variable1)
        quadsid = quadsid+1
        ret = ret + '\t\tadd $t0,$sp,-'+ str(s.offset) + '\n\t\tsw $t0,-8($fp)'
    elif quad.operetion == 'par' and quad.variable2 == 'REF':
        if quadsid ==0:
            for q in listofQuads:
                if q.quadid == quad.quadid:
                    num3 = -1
                elif num3 == -1 and q.operetion == 'call':
                    num3 = searchScope(q.variable1)
                    frameLength=num3.framelength
                    break
            ret = '\t\tadd $fp,$sp,' + str(frameLength) + '\n'
        else:
            ret = ''

        temp = 12 + 4 * quadsid
        quadsid = quadsid + 1
        v = searchScope(quad.variable1.strip())
        scope=scopeList[0]
        localVar=scope.varLocal(v.name)
        ret ='Error in ret'
        for scope in scopeList:
            if 1 == scope.varLocal(v.name):
                variableNesting=scope.nestingLevel

        if nesting == variableNesting or v.parMode == '' and localVar == 1:
            ret = '\t\tadd $t0,$sp,-'+ str(v.offset) + '\n\t\tsw $t0,-'+ str(temp) +'($fp)'
        elif nesting == variableNesting or v.parMode == 'inout':
            ret = '\t\tlw $t0,-'+str(v.offset)+'($sp)' +'\n\t\tsw $t0,-'+str(temp) +'($fp)'
        elif nesting != variableNesting or localVar ==1 or v.parMode == 'in':
            ret = gnlvcode(v.name) + '\t\tsw $t0,-' +str(temp) +'($fp)'
        elif nesting != variableNesting or v.parMode=='inout':
            ret = gnlvcode(v.name) + '\t\tlw $t0,($t0)' + '\n\t\tsw $t0,-' + str(temp) + '($fp)'
    elif quad.operetion == 'call':
        for scope in afterdeletscope:
            entityList= scope.returnListOfEntitys()
            for ent in entityList:
                if ent.name == quad.variable1 and quadsid >0:
                    i=scope.nestingLevel
                    quadsid=0
        frameLengthValu=searchScope(quad.variable1)
        if i == nesting:
            ret = '\t\tlw $t0,-4($sp)\n' + '\t\tsw $t0,-4($fp)\n'
        else:
            ret = '\t\tsw $sp,-4($fp)\n'

        ret =ret + '\t\tadd $sp,$sp,'+str(frameLengthValu.framelength) + '\n\t\tjal '+ quad.variable1 + '\n\t\tadd $sp,$sp,-'+ str(frameLengthValu.framelength) + '\n\t\tmove $t1,$v0\n' + storevar(1,'T_0')
    else:
        ret = "########Error no result in transforming mid to assembly"

    if flag == True:
        ret = '\tL_' + str(quad.quadid) + ': \n' + ret
    return ret


def generate_c_file(cFile):
    global listofQuads
    cFile.write('#include <stdio.h>\n\n\n')
    for quad in listofQuads:
        nq = transform_to_c(quad)
        cFile.write(nq +'                    //'+ "%s" % int(quad.quadid)+":"+str(quad.operetion)+"," +
                    str(quad.variable1)+","+str(quad.variable2)+","+str(quad.variable3)+ '\n')


def generate_finalCode_file(finalCodeFile):

    global quadsid
    quadsid = 0

    finalCodeFile.write('#------------------------------Global data as used in main \n')

    finalCodeFile.write('\t.text\n')
    finalCodeFile.write('\tj Lmain\n')
    for quad in listofQuads:
        nq = transform_to_finalCode(quad)
        finalCodeFile.write(nq +'\t\t# '+ "%s" % int(quad.quadid)+":"+str(quad.operetion)+"," +
                    str(quad.variable1)+","+str(quad.variable2)+","+str(quad.variable3)+ '\n')



class Entity:

    def __init__(self,name,typeofEntity,offset):
        self.name=str(name)
        self.typeofEntity=str(typeofEntity)
        self.offset = offset
        self.startQuad = 0
        self.parMode = ""
        self.listOFArguments = []
        self.nextEntity= 0
        self.varType = "int"
        self.framelength = 0
    def setframelength(self,fl):
        self.framelength=fl
    def setVarType(self,vType):
        self.varType = vType

    def setEntity(self,nextE):
        self.nextEntity=nextE

    def setParMode(self,par):
        self.parMode=par

    def setArgument(self,nextA):
        self.listOFArguments.append(nextA)

    def setstartQuad(self,starQ):
        self.startQuad=starQ

    def changeoffset(self,newoffset):
        self.offset=newoffset

    def returnoffset(self):
        return self.offset

    def returnArgL(self):
        return self.listOFArguments

    def printer(self):
        print('Name:',self.name + ":" + "Offset " +str(self.offset) + " Type of entity "+self.typeofEntity+ " Par "+self.parMode)
        if self.typeofEntity == "function":
            print("NextQuad",self.startQuad,"Framelength",self.framelength)

class Scope:
    def __init__(self,nestingLevel):
        self.nestingLevel=nestingLevel
        self.listofEntitys = []
        self.enclosingScope = False

    def setScopeClosed(self):
        self.enclosingScope = True

    def addentity(self,entitytoadd):
        self.listofEntitys.append(entitytoadd)

    def printScope(self):
        print(self.nestingLevel)

    def setListOfEntitys(self,entLi):
        self.listofEntitys=entLi

    def getTotalOffset(self):
        if len(self.listofEntitys)==0:
            return 0
        else:
            ent=self.listofEntitys[-1]
            entsoff=ent.returnoffset()
            return entsoff

    def returnListOfEntitys(self):
        return self.listofEntitys

    def varLocal(self,Varname):
        for x in self.listofEntitys:
            if x.name == Varname.strip():
                return 1

        return 0

class Argument:
    global argumentuniqeID
    argumentuniqeID=argumentuniqeID+1
    def __init__(self,parMode,typeOfArg):
        self.parMode=parMode
        self.typeofArgument = typeOfArg
        self.argumentID=argumentuniqeID
        self.nextArgument =0

    def compare(self,arg2):
        result=True
        if self.parMode!=arg2.parMode:
            result= False
        return result
    def printerArg(self):
        print(str(self.parMode)+"   ")

    def tonextArgument(self,nextArg):
        self.nextArgument=nextArg


def searchScope(searchElement):
    vforreturn =Entity("Fail",'int',0)
    nameTostrip = ''
    for scope in scopeList:
        entititiesList=scope.returnListOfEntitys()
        for enti in entititiesList:
            if enti.name==searchElement:
                #vforreturn = enti.name
                vforreturn=enti
                nameTostrip = vforreturn.name
                nameTostrip.strip()
                vforreturn.name = nameTostrip
            elif searchElement.isdigit():
                vforreturn.name=searchElement
    ###alages gia thn epistrofh san antikimeno enity kai alages ekei pou xrisimopiousame thn synarthsh


    return vforreturn


def checkSymasiologikh(): ##elexoi
    ##elexoi gia to an exoun oles oi funtions return
    for x in functionL:
        if functionL[x]==0:
            print("Function with no return found the funtion is",functionL[x])
            sys.exit()
    ##elexoi an otan kaloume mia synarthsh an einai idoi oi parametoi kai me thn idia seira
    for x in listofFuncPars:
        for y in afterdeletscope:
            ma=y.returnListOfEntitys()
            for z in ma:
                if x.name==z.name:
                    if len(z.returnArgL())==len(x.returnArgL()):
                        i=0
                        zz=z.returnArgL()
                        xx=x.returnArgL()
                        while(i<len(z.returnArgL())):
                            za=zz[i]
                            xa=xx[i]
                            if za.parMode != xa.parMode :
                                print("Detected a wrong parameter in funtion ",x.name)
                                sys.exit()
                            i=i+1
                    else:
                        print("Detected a wrong parameter in funtion ",x.name," ")
                        sys.exit()

    ##kanei update ola ta framelength
    for x in afterdeletscope:
        xlist=x.returnListOfEntitys()
        entiFunc = xlist[0]
        lastoffset= xlist[-1]
        entiFunc.setframelength(x.getTotalOffset())
        xlist[0]=entiFunc
        for y in afterdeletscope:
            ylistofentity=y.returnListOfEntitys()
            for yl in ylistofentity:
                if entiFunc.name==yl.name:
                    yl.setframelength(x.getTotalOffset())



def printSymbolTable():## kanei print ta scopes
    for xo in afterdeletscope:
        print("\n---------------------------------------------")
        xo.printScope()
        print('\n=======================')
        ls=xo.returnListOfEntitys()
        for l in ls:
            l.printer()
            a=l.returnArgL()
            for arg in a:
                arg.printerArg()
        print("---------------------------------------------")


##apo edw kai katw anoigoume ta files,kleinoume ta files,kai kalountai oi apparethtes synarthshs gia thn leitourgia
user_args=sys.argv[1]
file = io.open(user_args,mode='r',encoding="UTF-8")


syntaktikos_analyths()
checkSymasiologikh()
#printSymbolTable() #kanei print to pinaka symbolon sthn arxh ka8e scope an einai synarthsh yparxei to onoma ths kai ta details ths
user_args=user_args[:-4]
scopeList=afterdeletscope.copy()
##grafei to mid code se file

midocdeFiletoWrite=user_args + ".int"
with open(midocdeFiletoWrite, 'w') as midcode:
    for item in listofQuads:
        midcode.write("%s" % int(item.quadid)+":"+str(item.operetion)+"," +
                    str(item.variable1)+","+str(item.variable2)+","+str(item.variable3))
        midcode.write("\n")
# ME BASH TA EXAMPLE1 2 KAI 3 POU YPIRXANE ME THN EKFWNHSH THS ASKHSHS KAI THS INCASE KAI FORCASE POU VALAME GIA DOKIMH TREXEI KANONIKA

finaclCodeFile = user_args+".asm"
fCode= open(finaclCodeFile,'w')
generate_finalCode_file(fCode)
scopeList=afterdeletscope.copy()

cfile=user_args+".c"
cFile = open(cfile, 'w')
generate_c_file(cFile)

file.close()
midcode.close()
cFile.close()
fCode.close()
print("Succesfull compile")
