from enum import Enum

STATEMENT_TYPE = "type"

ACTION = 'action'

EXECUTE = "execute"

MEMORY = "memory"

class Statement(Enum):
    ACTION_STATEMENT = "action_statement"
    MEMORY_STATEMENT = "memory_statement"
    EXECUTE_STATEMENT = "execution_statement"
    PIPELINE_STATEMENT = "pipeline_statement"
    SWITCH_STATEMENT = "switch_statement"
    LOOP_STATEMENT = "loop_statement"