# Main component which address pipeline geterogenity problem

# |input(validator) -> model -> (exception)output|  -> bridge | input(validator).... 

class Bridge():
    def parseConnection(self):
        str = "a->b; apple->input:"
        print(str)
        pass


class Transformer(Bridge):
    pass


