from __future__ import annotations
from typing import  Dict, Any, List, Optional, Union, cast, Callable
import logging
import copy

from core.executable_level_1.eval import (
    Condition, 
    ExecutionSchema, 
    IfStatement, 
    While,
    Filter,
    ForEach,
)
from core.executable_level_1.memory import (
    GetMemory, 
    MemoryGetInstruction,  
    MemoryManager, 
    # MemorySetInstruction, 
    SetMemory
)
from core.executable_level_1.statements_types import Statement
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Config, Input, Output, Transformable
)
from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
# from core.executable_level_1.utils import generate_unique_state

EvaluatorLogger = logging.Logger("EvaluatorLogger", logging.INFO)

INPUT = "input"

class EvaluatorConfigs():
    pass


class Evaluator:
    program: List[Dict[str, Any]]  # Corrected typo in 'retrieve'
    memory_manager: MemoryManager
    register: Transformable
    
    def __init__(
        self, 
        schema: ExecutionSchema, 
        cfg: EvaluatorConfigs = EvaluatorConfigs()
    ) -> None:
        self.program = schema.retrieve_program()  # Corrected typo in 'retrieve'
        self.memory_manager = MemoryManager(None)


    def prepare_input(
        self, 
        program_input: Optional[
            Union[Dict[str, Any], List[Dict[str, Any]]]
        ]
    ) -> Transformable:
        """Sets the initial input for the program."""
        if program_input is not None:
            return Transformable(program_input)  # Assuming this method correctly instantiates a Transformable
        return Transformable({})


    def run_program(
        self, 
        program_input: Optional[
            Union[Dict[str, Any], List[Dict[str, Any]]]
        ]
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:    
        return self.eval_program(
            self.program,
            self.prepare_input(program_input)
        ).extract()
    
    
    def eval_program(
        self, 
        program: List[Dict[str, Any]], 
        program_input: Transformable
    ) -> Transformable:
        """Evaluates the program based on the input provided."""
        for i, st in enumerate(program):
            try:
                self.eval(st, program_input)
                EvaluatorLogger.info(f"Step {i} executed successfully.")
            except Exception as e:
                EvaluatorLogger.error(f"Error at step {i}: {e}")
                EvaluatorLogger.exception(e)
        return self.register


    def eval(
        self, st: Dict[str, Any], input_data: Transformable
    ) -> Transformable:
        """Evaluates a single statement."""
        if st["type"] == Statement.EXECUTE_STATEMENT:
            comp = st[Statement.EXECUTE_STATEMENT.value]
            return self.eval_execute(comp, input_data)  # Assuming comp is an executable; this needs to match the method definition
        elif st["type"] == Statement.ACTION_STATEMENT:
            comp = st[Statement.ACTION_STATEMENT.value]
            return self.eval_action(comp, input_data)  # Assuming comp is an action; this needs to match the method definition
        elif st["type"] == Statement.SET_MEMORY_STATEMENT:
            comp = st[Statement.SET_MEMORY_STATEMENT.value]
            return self.eval_set_memory(comp, input_data)
        elif st["type"] == Statement.GET_MEMORY_STATEMENT:
            comp = st[Statement.GET_MEMORY_STATEMENT.value]
            return self.eval_get_memory(comp, input_data)
        elif st["type"] == Statement.PIPELINE_STATEMENT:
            comp = st[Statement.PIPELINE_STATEMENT.value]
            return self.eval_pipeline(comp, input_data)
        # elif st["type"] == Statement.CONDITION:
        #     comp = st[Statement.CONDITION.value]
        #     self.eval_if_statement(comp)
        elif st["type"] == Statement.IF_STATEMENT:
            comp = st[Statement.IF_STATEMENT.value]
            return self.eval_if_statement(comp, input_data)
        elif st["type"] == Statement.FILTER_STATEMENT:
            comp = st[Statement.FILTER_STATEMENT.value]
            return self.eval_filter_statement(comp, input_data)
        raise ValueError(f"Unexpected statement type!: {st['type']}")


    def eval_action(
        self, 
        action: Action[InputState, OutputState],
        input_data: Transformable
    ) -> Transformable:
        """Evaluates an action statement."""
        # Update the register state based on the action
        input_data.update_state(action)
        return input_data


    def eval_execute(
        self, 
        executable: Executable[Config, Input, Output],
        input_data: Transformable
    ) -> Transformable:
        """Evaluates an execute statement."""
        # Execute the executable and update the register accordingly
        if input_data.is_batch:
            return executable.execute_batch(input_data)
        return executable.execute(input_data)
    
    
    def eval_set_memory(
        self, 
        set_memory_command: SetMemory,
        input_data: Transformable
    ) -> Transformable:
        return self.memory_manager.resolve_set_memory(set_memory_command, input_data)
    
    def eval_get_memory(
        self, 
        get_memory_command: GetMemory,
        input_data: Transformable
    ) -> Transformable:
        return self.memory_manager.resolve_get_memory(
            get_memory_command, 
            input_data
        )
    
    
    def eval_pipeline(
        self, 
        pipeline: List[Dict[str, Any]],
        input_data: Transformable
    ) -> Transformable:
        return self.eval_program(pipeline, input_data)


    # def eval_condition(self, condition: Condition):
    #     unique_state = generate_unique_state()
    #     set_commend = self.memory_manager.generate_set_command(unique_state, MemorySetInstruction.SET_AND_FLUSH)
    #     self.memory_manager.resolve_set_memory(set_commend, self.register)
    #     work_state = condition.get_state()
    #     if work_state != None:
    #         get_command = self.memory_manager.generate_get_memory_command(work_state, MemoryGetInstruction.GET_AND_GO)
    #         self.register = self.memory_manager.resolve_get_memory(get_command, self.register)
    #     st = condition.get_statement()
    #     self.eval(st)
    #     validator = condition.get_validator()
    #     res = validator(self.register)
    #     old_state_get  = self.memory_manager.generate_get_memory_command([unique_state], MemoryGetInstruction.FLUSH_AND_GET)
    #     self.register = self.memory_manager.resolve_get_memory(old_state_get, self.register)
    #     return res
        
    def eval_condition(
        self, 
        condition: Union[Callable[[Transformable], bool], Condition],
        input_data: Transformable
    ) -> bool:
        if isinstance(condition, Condition):
            work_state = condition.get_state()
            if work_state != None:
                get_command = self.memory_manager.generate_get_memory_command(
                    work_state, MemoryGetInstruction.GET_AND_GO
                )
                input_data = self.memory_manager.resolve_get_memory(
                    get_command, input_data
                )
            ev = Evaluator(condition.get_statement())
            input_data = ev.eval_program(
                ev.program,
                copy.deepcopy(input_data)
            )
            return condition.validator(input_data)
        elif callable(condition):
            return condition(copy.deepcopy(input_data))
        else:
            raise Exception()
    

    def eval_if_statement(
        self, 
        if_statement: IfStatement,
        input_data: Transformable
    ) -> Transformable:
        bool_flag = self.eval_condition(
            condition=if_statement.get_condition(),
            input_data=input_data
        )
        
        if bool_flag == True:
            right_stetement = if_statement.get_right_statement()
            return self.eval(
                right_stetement, input_data
            )
        else:
            left_stetement = if_statement.get_left_statement()
            if left_stetement == None:
                return input_data
            return self.eval(
                left_stetement, input_data
            )


    def eval_while_statement(
        self, while_statement: While, input_data: Transformable
    ) -> Transformable:
        retries = while_statement.get_retries()
        if retries == None:
            while self.eval_condition(
                while_statement.get_condition(), 
                input_data
            ):
                input_data = self.eval(
                    while_statement.get_statement(),
                    input_data
                )
        else:
            while (
                self.eval_condition(
                    while_statement.get_condition(),
                    input_data
                ) and retries > 0
            ):
                input_data = self.eval(
                    while_statement.get_statement(),
                    input_data
                )
                retries -= 1
        return input_data


    def eval_filter_statement(
        self, filter_statement: Filter, input_data: Transformable
    ) -> Transformable:
        return Transformable([
            s for s in self.register
            if self.eval_condition(
                filter_statement.get_condition(),
                Transformable(s)
            )
        ])

    
    def eval_for_each(self, for_each_statement: ForEach) -> Transformable:
        return Transformable([
            cast(
                Dict[str, Any],
                Evaluator(for_each_statement.get_statement()).run_program(t)
            ) for t in self.register
        ])

# class EvaluatorCycleEvaluator:
#     # for cyclic constructs
#     initial_input: str
#     chunks: List[str]
#     offset: int 
#     round: int



# !!!!restart and other intresting stuff

# class Node:
#     def __init__(self, action, children=None, restart=False, offset=None):
#         self.action = action  # The action to be executed
#         self.children = children if children is not None else []
#         self.restart = restart  # Whether this node triggers a restart
#         self.offset = offset  # Optional offset for restarts




# class LoopNode(Node):
#     def __init__(self, loop_condition, child: Node, **kwargs):
#         super().__init__(action=None, **kwargs)  # Loop node doesn't have a direct action
#         self.loop_condition = loop_condition  # Can be a function or a fixed integer
#         self.child = child

#     def execute(self, memory: Memory, input_data: Any = None):
#         if isinstance(self.loop_condition, int):  # Fixed number of iterations
#             for _ in range(self.loop_condition):
#                 input_data = self.child.execute(memory, input_data)
#         else:  # Assume loop_condition is a callable for dynamic evaluation
#             while self.loop_condition(input_data):
#                 input_data = self.child.execute(memory, input_data)
#         return input_data



# def create_statement(action):
#     return {"statement": action}

# def create_conditional(condition, true_branch, false_branch=None):
#     return {
#         "if": {
#             "condition": condition,
#             "true_branch": true_branch,
#             "false_branch": false_branch or []
#         }
#     }

# def create_loop(condition, body):
#     return {
#         "loop": {
#             "condition": condition,
#             "body": body
#         }
#     }


# !!!!!!!!




# class Command(ABC):
#     def __init__(self, evaluator: Evaluator) -> None:
#         self.evaluator = evaluator


#     @abstractmethod
#     def __call__(
#         self, task: Any
#     ) -> Evaluator:
#         ...


# class ActionCommand(Command):
#     def __call__(
#         self, task: Action
#     ) -> Evaluator:
#         self.evaluator.state = task.execute(self.evaluator.state)
#         return self.evaluator


# class MemoryCommand(Command):
#     def __call__(
#         self, task: Component, task2: Component
#     ) -> Evaluator:
#         ...

 



# class PipelineCommand(Command):
#     def __call__(
#         self, task: List[Dict[Statement, Any]]
#     ) -> Evaluator:
#         for stage in task:
#             for statement, sub_task in stage.items():
#                 self.evaluator[statement](sub_task)

#         return self.evaluator


# class SwitchCommand(Command):
#     def __call__(
#         self, 
#         task: List[
#             Tuple[
#                 Callable[[Dict[str, Any]], bool], 
#                 Dict[Statement, Any]
#             ]
#         ]
#     ) -> Evaluator:
#         # TODO: multiple exits
#         for check, stage in task:
#             if check(self.evaluator.state):
#                 for statement, sub_task in stage.items(): 
#                     self.evaluator[statement](sub_task)
#                 break
#         return self.evaluator


# class LoopCommand(Command):
#     def __call__(
#         self, task: List[Dict[Statement, Any]]
#     ) -> Evaluator:
#         while condition:
#             for stage in task:
#                 for statement, sub_task in stage.items(): 
#                     self.evaluator[statement](sub_task)
#         return self.evaluator