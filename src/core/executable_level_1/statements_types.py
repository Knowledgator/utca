from enum import Enum

STATEMENT_TYPE = "type"

ACTION = 'action'

EXECUTE = "execute"

MEMORY = "memory"

class Statement(Enum):
    ACTION_STATEMENT = "action_statement"
    MEMORY_STATEMENT = "memory_statement"
    EXECUTE_STATEMENT = "execution_statement"
    GET_MEMORY_STATEMENT = "get_memory_statement"
    SET_MEMORY_STATEMENT = "set_memory_statement"
    PIPELINE_STATEMENT = "pipeline_statement"
    CONDITION = "condition"
    IF_STATEMENT = "if_statement"
    WHILE_STATEMEMT = "while_statement"
    FOR_EACH_STATEMENT = "for_each_statement"
    FILTER_STATEMENT = "filter_statement"
    # SWITCH_STATEMENT = "switch_statement"
    # LOOP_STATEMENT = "loop_statement"
    # PARALLEL_STATEMENT = "parallel_statement"