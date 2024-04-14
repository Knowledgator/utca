class ActionError(Exception):
    def __init__(self, action_class: str, e: Exception):
        super().__init__(f"Action error: {action_class}: {e}")


class InputSchemaNotFound(Exception):
    def __init__(self, message: str="InputSchemaNotFound"):
        self.message = message
        super().__init__(self.message)


class OutputSchemaNotFound(Exception):
    def __init__(self, message: str="OutputSchemaNotFound"):
        self.message = message
        super().__init__(self.message)


class ExecutionSchemaInvalidFirstComponent(Exception):
    def __init__(self, message: str="First component should be executable or input"):
        self.message = message
        super().__init__(self.message)


class ExecutionSchemaInvalidFlow(Exception):
    def __init__(self, message: str="Last executable can not be null"):
        self.message = message
        super().__init__(self.message)


class EvaluatorExecutionFailed(Exception):
    def __init__(self, e: Exception):
        super().__init__(f"Program failed! {e}")


class InavalidMemoryInstruction(ValueError):
    ...


class IvalidInputDataValue(ValueError):
    ...