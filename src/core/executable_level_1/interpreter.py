

class Evaluator():
    program: PROGRAM
    transferable_checkpoint: Transformable
    memory: Memory
    # state saver for each stage, stage_name, command -> result

    def __init__(self, schema: ExecutionSchema, cfg: EvaluatorConfigs = EvaluatorConfigs()) -> None:
        self.program = schema.retieve_program()
        self.memory = Memory()
    
    def run(self, program_input: Input):
        # execution loop
        for i, st in enumerate(self.program):
            if i == 0:
                self.execute_input_statement(st, program_input)
            else:
                self.execute_ordinary_statement(st)
            print("Executed step: ", i)
        return self.transferable_checkpoint.extract()
    

    def execute_ordinary_statement(self, statement: TRANSFORM_STATEMENT):
        for el in statement:
            if  isinstance(el, Executable):
                self.transferable_checkpoint = el.execute(self.transferable_checkpoint, Transformable)
            else:
                self.transferable_checkpoint.update_state(el)


    def execute_input_statement(self, statement: INPUT_STATEMENT, input: Input):
        executable = statement[0]
        self.transferable_checkpoint = executable.execute(input, Transformable)


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




# program_structure = {
#     "start": [
#         {"statement": lambda ctx: print("Statement 1 execution", ctx)},
#         {"statement": lambda ctx: print("Statement 2 execution", ctx)},
#         {"if": {
#             "condition": lambda ctx: ctx["condition"],
#             "true_branch": [
#                 {"statement": lambda ctx: print("True branch statement", ctx)}
#             ],
#             "false_branch": [
#                 {"statement": lambda ctx: print("False branch statement", ctx)}
#             ]
#         }},
#         {"loop": {
#             "condition": lambda ctx: ctx["loop_condition"](),
#             "body": [
#                 {"statement": lambda ctx: print("Loop body statement", ctx) or ctx["loop_actions"]()}
#             ]
#         }}
#     ]
# }

# !!!!!!!!!!

# class InputStatement()
#     ex: Executable
#     tr: Transforms