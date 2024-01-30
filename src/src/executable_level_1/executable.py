from ast import Dict
from abc import ABC, abstractmethod


INPUT_SCHEMA_PATH = "/io/input_schema.json"
OUTPUT_SCHEMA_PATH = "/io/output_schema.json"

# InputType = TypeVar('InputType') # can be send more general
# OutputType = TypeVar('OutputType')


class IOValidator(ABC):
    def __init__(self, path: str = ".") -> None:
        # work with input schema
        input = loadSchema(path + INPUT_SCHEMA_PATH)
        self.inputSchema =  parseInputSchema(input)

        # work with output schema 
        output = loadSchema(path + OUTPUT_SCHEMA_PATH)
        self.outputSchema = SchemaparseInputSchema(input)
    def loadSchema(self, path: str =".") -> str:
        with open(path, "r") as file:
            content = file.read()
            self.parse(content)
    def parse(self, content: str):
        # Implement parsing logic
        pass
    def parseInputSchema(self):
        self.parse()
        pass
    def parseOutputSchema(self):
        self.parse()
        pass
    @abstractmethod
    def isValidInput(self) -> bool:
        pass
    @abstractmethod
    def isValidOutput(self) -> bool:
        pass



# потом дженерик можно заменить на что то subtyped
class Executable(ABC):

    def __init__(self, isValidatoring: bool, validator: IOValidator):
        self.validator = validator
        self.isValidating = isValidatoring
    def execute(self, input_data: Dict) -> OutputType:
        if  self.isValidating:

            if not self.validator.isValidInput(input_data):
                raise ValueError("Invalid input")
            result = self.invoke(input_data)
            if not self.validator.isValidOutput(result):
                raise ValueError("Invalid output")
            return result
        else:
            result = invoke(input_data)
        return result

    @abstractmethod
    def invoke(self, input_data: Dict) -> Dict:
        pass

