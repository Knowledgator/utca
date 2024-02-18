from __future__ import annotations
from typing import Dict, Any, List, Optional

from core.executable_level_1.eval import ExecutionSchema
from core.executable_level_1.memory import Memory

from core.executable_level_1.statements_types import Statement
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Config, Input, Output, Action, Transformable
)


INPUT = "input"

class EvaluatorConfigs():
    pass



class Evaluator:
    program: List[Dict[str, Any]]  # Corrected typo in 'retrieve'
    memory = Memory()
    transferable_checkpoint: Transformable
    def __init__(self, schema: ExecutionSchema, cfg: EvaluatorConfigs = EvaluatorConfigs()) -> None:
        self.program = schema.retrieve_program()  # Corrected typo in 'retrieve'
        self.memory = Memory()
        self.transferable_checkpoint: Transformable = Transformable({})  # Initialized but must be set properly

    def set_initial_input(self, program_input: Input) -> None:
        """Sets the initial input for the program."""
        self.transferable_checkpoint = program_input.generate_transformable()  # Assuming this method correctly instantiates a Transformable

    def eval_program(self, program_input: Optional[Input] = None) -> Any:
        """Evaluates the program based on the input provided."""
        if program_input is not None:
            self.set_initial_input(program_input)
        # Execution loop
        for i, st in enumerate(self.program):
            try:
                self.eval(st)
            except Exception as e:
                print(f"Error at step {i}: {e}")
        return self.transferable_checkpoint.extract()  # Assuming this method extracts the final result

    def eval(self, st: Dict[str, Any]) -> None:
        """Evaluates a single statement."""
        if st["type"] == Statement.EXECUTE_STATEMENT:
            comp = st[Statement.EXECUTE_STATEMENT.value]
            self.eval_execute(comp)  # Assuming comp is an executable; this needs to match the method definition
        elif st["type"] == Statement.ACTION_STATEMENT:
            comp = st[Statement.ACTION_STATEMENT.value]
            self.eval_action(comp)  # Assuming comp is an action; this needs to match the method definition

    def eval_action(self, action: Action) -> None:
        """Evaluates an action statement."""
        # Update the transferable_checkpoint state based on the action
        self.transferable_checkpoint.update_state(action)

    def eval_execute(self, executable: Executable[Config, Input, Output]) -> None:
        """Evaluates an execute statement."""
        # Execute the executable and update the transferable_checkpoint accordingly
        self.transferable_checkpoint = executable.execute(self.transferable_checkpoint, Transformable)

    
    #### memory handling 

   
    # def execute_ordinary_statement(self, statement: TRANSFORM_STATEMENT):
    #     for el in statement:
    #         if  isinstance(el, Executable):
    #             self.transferable_checkpoint = el.execute(self.transferable_checkpoint, Transformable)
    #         else:
    #             self.transferable_checkpoint.update_state(el)


    # def execute_input_statement(self, statement: INPUT_STATEMENT, input: Input):
    #     executable = statement[0]
    #     self.transferable_checkpoint = executable.execute(input, Transformable)




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