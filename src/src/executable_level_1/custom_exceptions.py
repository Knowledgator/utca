
class InputSchemaNotFound(Exception):
    def __init__(self, message: str="InputSchemaNotFound"):
        self.message = message
        super().__init__(self.message)


class OutputSchemaNotFound(Exception):
    def __init__(self, message: str="OutputSchemaNotFound"):
        self.message = message
        super().__init__(self.message)