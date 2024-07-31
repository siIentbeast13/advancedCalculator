from tokens import *
from lexer import Token
from debug import log



class Segment:
    value:int = 0

    def __repr__(self) -> str:
        return f"Segment({self.rawData} = {self.value})"

    def __init__(self, rawData:list[Token]) -> None:
        log("parser:class.Segment initialized")
        self.rawData = rawData 

    def process(self):
        bracketCount = 0
        output = []
        buffer = []
        for token in self.rawData:
            log(f"parser:class.Segment:function.process processing: {token}")
            if bracketCount:
                if token.type == BRACSTART_T:
                    bracketCount += 1
                    buffer.append(token)

                elif token.type == BRACEND_T:
                    bracketCount -= 1
                    if bracketCount:
                        buffer.append(token)
                        continue

                    numCount = 0
                    for t in buffer:
                        if t.type == NUM_T:
                            numCount += 1
                    
                    if not numCount:
                        print("Syntax error")
                        exit()

                    newSeg = Segment(buffer)
                    output.append(newSeg)
                    buffer = []
                    newSeg.process()

                else:
                    buffer.append(token)

            else:
                if token.type == BRACSTART_T:
                    bracketCount += 1
                else:
                    output.append(token)
        
        log("parser:class.Segment:function.process finished inner-segment creation and processing: "+str(output))

        #
        # arithmetic processing
        #
        # handle subtraction operator
        output2:list[Token] = []

        i = 0
        while i < len(output):
            if type(output[i]) == Segment:
                print("Segment")
                output2.append(Token(NUM_T, output[i].value))
            elif output[i].type == SUB_T:
                if type(output[i+1]) == Segment:
                    output2.append(Token(NUM_T, -output[i+1].value))
                elif output[i+1].type == NUM_T:
                    output2.append(Token(NUM_T, -output[i+1].value))
                else:
                    print("Syntax error")
                    exit()
                i += 1
            elif output[i].type != ADD_T:
                output2.append(output[i]) 

            i += 1
        
        log("parser:class.Segment:function.process Subtraction and addition operator handled: "+str(output2))
        output2.append(None)
        del output
        

        # division

        if output2[0].type in [MUL_T, DIV_T]:
            print("Syntax error")
            exit()


        for t in output2:
            if not t:
                break
            if t.type != DIV_T:
                continue

            i = 0
            output3:list[Token] = []
            while i < len(output2):
                if not output2[i]:
                    break

                if output2[i+1]:
                    if output2[i+1].type == DIV_T:
                        if not output2[i+2]:
                            print("Syntax error")
                            exit()
                        
                        if output2[i].type != NUM_T or output2[i+2].type != NUM_T:
                            print("Syntax error")
                            exit()
                        
                        if not output2[i+2].value:
                            print("Cannot divide by zero")
                            exit()
                        
                        output3.append(Token(NUM_T, output2[i].value / output2[i+2].value))

                        i+=3
                        continue
                output3.append(output2[i])

                i += 1
            
            output2 = output3.copy()
            output2.append(None)

        log("parser:class.Segment:function.process finished division: "+str(output2))


        #multiplication
        for t in output2:
            if not t:
                break
            if t.type != MUL_T:
                continue

            output3:list[Token] = []

            i = 0
            while i < len(output2):
                if not output2[i]:
                    break

                if output2[i+1]:
                    if output2[i+1].type == MUL_T:
                        if not output2[i+2]:
                            print("Syntax error")
                            exit()

                        if output2[i].type != NUM_T or output2[i+2].type != NUM_T:
                            print("Syntax error")
                            exit()
                        
                        output3.append(Token(NUM_T, output2[i].value * output2[i+2].value))
                        
                        i += 3
                        continue

                output3.append(output2[i])

                i += 1
            
            output2 = output3.copy()
        
        log("parser:class.Parser:function.process finished multiplication: "+str(output2))

        for numToken in output2:
            if numToken:
                self.value += numToken.value
        
        log("parser:class.Parser:function.process finished segment processing: "+str(self.value))