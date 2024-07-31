from debug import *
import time
import lexer
import parser



def main() -> None:
    global start


    code:str = input("> ").replace(" ","")

    start = time.time()

    log("main:function.main input: "+code)

    for c in code:
        if c not in "1234567890()-+*/":
            print("Invalid character")
            exit()

    lex = lexer.Lexer(code)
    lex.start()
    tokens = lex.output

    rootSegment = parser.Segment(tokens)
    rootSegment.process()

    print(f"= {rootSegment.value}")



if __name__ == "__main__":
    main()

    if DEBUG : print(f"(-) Time taken: {time.time()-start}s")