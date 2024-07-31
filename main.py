from debug import *
import time
import lexer
import parser



def main() -> None:
    global start


    code:str = input("> ")

    start = time.time()

    log("main:function.main input: "+code)


    lex = lexer.Lexer(code.replace(" ", ""))
    lex.start()
    tokens = lex.output

    rootSegment = parser.Segment(tokens)
    rootSegment.process()

    print(f"= {rootSegment.value}")



if __name__ == "__main__":
    main()

    if DEBUG : print(f"(-) Time taken: {time.time()-start}s")