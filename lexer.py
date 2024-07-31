from debug import log 
from tokens import *




class Token:
    def __init__(self, type:int, value:float=None) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"NUM_T({self.value})"
        return TYPE_NAMES[self.type]


class Lexer:
    data:str = ""
    last:str = ""
    current:str = ""
    specialChars:str = "+-*/()"
    syntax:list[str] = []
    output:list[Token] = []
    index:int = 0



    def __init__(self, data) -> None:
        self.data = data

        log("lexer:class.Lexer initialized")
    

    def pushLast(self) -> None:
        if not self.last:
            return
        
        self.syntax.append(self.last)
        self.last = ""
    


    def start(self) -> None:
        if "()" in self.data:
            print("Syntax error")
            exit()

        self.current = self.data[0]

        while self.index < len(self.data):
            self.current = self.data[self.index]
            log(f"lexer:class.Lexer:function.start processing: {self.current}")

            if self.current in self.specialChars:
                self.pushLast() 
                self.syntax.append(self.current)
            else:
                self.last += self.current

            self.index += 1
        
        self.pushLast()


        log("lexer:class.Lexer:function.start finished processing: "+str(self.syntax))


        lastTokenIsNum = False # To add * automatically before a bracket when no operators are infront of it
        bracC = 0
        for element in self.syntax:
            log("lexer:class.Lexer:function.start naming: "+element)
            try:
                self.output.append(Token(NUM_T, float(element)))
                lastTokenIsNum = True 
            except:
                if element == "+":
                    self.output.append(Token(ADD_T))
                elif element == "-":
                    self.output.append(Token(SUB_T))
                elif element == "*":
                    self.output.append(Token(MUL_T))
                elif element == "/":
                    self.output.append(Token(DIV_T))
                elif element == "(":
                    if lastTokenIsNum:
                        self.output.append(Token(MUL_T))
                    self.output.append(Token(BRACSTART_T))
                    bracC += 1
                elif element == ")":
                    self.output.append(Token(BRACEND_T))
                    bracC -= 1
                    lastTokenIsNum = True
                    continue
                
                lastTokenIsNum = False
        if bracC:
            print("Syntax error: mismatched brackets")
            exit()
        
        log("lexer:class.Lexer:function.start finished naming: " + str(self.output))