from __future__ import annotations
from typing import (
    Dict, Any, List, Callable, Optional, Union, cast
)
import logging
import copy

from core.executable_level_1.component import Component
from core.executable_level_1.executor import Executor
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
    SetMemory,
    DeleteMemory,
    MemoryGetInstruction,  
    MemoryManager, 
)
from core.executable_level_1.statements_types import Statement
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Input, Output, Transformable
)
from core.executable_level_1.actions import Action
from core.executable_level_1.exceptions import (
    EvaluatorExecutionFailed
)

INPUT = "input"

class EvaluatorConfigs:
    logging_level: int
    logging_handler: logging.Handler
    logger: logging.Logger
    fast_exit: bool

    def __init__(
        self,
        name: str="Evaluator", 
        logging_level: int=logging.INFO,
        logging_handler: Optional[logging.Handler]=None,
        fast_exit: bool=True
    ):
        self.name = name
        self.logging_level = logging_level
        self.logging_handler = logging_handler or logging.StreamHandler()
        self.logger = logging.Logger(
            self.name, 
            self.logging_level
        )
        self.logger.addHandler(self.logging_handler)
        self.fast_exit = fast_exit


class Evaluator:
    program: List[Component]
    memory_manager: MemoryManager
    
    def __init__(
        self, 
        schema: ExecutionSchema, 
        cfg: Optional[EvaluatorConfigs]=None,
    ) -> None:
        self.cfg = cfg or EvaluatorConfigs()
        self.program = schema.retrieve_program()  # Corrected typo in 'retrieve'
        self.memory_manager = MemoryManager(None)


    def prepare_input(
        self, 
        program_input: Optional[Dict[str, Any]]=None
    ) -> Transformable:
        """Sets the initial input for the program."""
        if program_input is not None:
            return Transformable(program_input)  # Assuming this method correctly instantiates a Transformable
        return Transformable({})


    def run_program(
        self, 
        program_input: Optional[Dict[str, Any]]=None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:    
        return self.eval_program(
            self.program,
            self.prepare_input(program_input),
            self.cfg.logger.name
        ).extract()
    
    
    def eval_program(
        self, 
        program: List[Component], 
        program_input: Transformable,
        evaluator_name: str
    ) -> Transformable:
        """Evaluates the program based on the input provided."""
        for i, st in enumerate(program):
            try:
                program_input = self.eval(st, program_input, evaluator_name)
                self.cfg.logger.info(f"{evaluator_name}: Step {i} executed successfully.")
            except Exception as e:
                self.cfg.logger.error(f"{evaluator_name}: Error at step {i}")
                self.cfg.logger.exception(e)
                if self.cfg.fast_exit:
                    raise EvaluatorExecutionFailed(e)
        return program_input


    def eval(
        self, 
        st: Component, 
        input_data: Transformable,
        evaluator_name: str
    ) -> Transformable:
        """Evaluates a single statement."""
        if st.statement == Statement.EXECUTE_STATEMENT:
            return self.eval_execute(
                cast(Executable[Input, Output], st), 
                input_data
            )
        elif st.statement == Statement.ACTION_STATEMENT:
            return self.eval_action(
                cast(Action[Any, Any], st),
                input_data
            )
        elif st.statement == Statement.SET_MEMORY_STATEMENT:
            return self.eval_set_memory(
                cast(SetMemory, st), 
                input_data
            )
        elif st.statement == Statement.GET_MEMORY_STATEMENT:
            return self.eval_get_memory(
                cast(GetMemory, st), 
                input_data
            )
        elif st.statement == Statement.DELETE_MEMORY_STATEMENT:
            return self.eval_delete_memory(
                cast(DeleteMemory, st), 
                input_data
            )
        elif st.statement == Statement.PIPELINE_STATEMENT:
            return self.eval_pipeline(
                cast(ExecutionSchema, st), 
                input_data, 
                evaluator_name
            )
        elif st.statement == Statement.IF_STATEMENT:
            return self.eval_if_statement(
                cast(IfStatement, st), 
                input_data,
                evaluator_name
            )
        elif st.statement == Statement.FILTER_STATEMENT:
            return self.eval_filter_statement(
                cast(Filter, st), 
                input_data
            )
        elif st.statement == Statement.FOR_EACH_STATEMENT:
            return self.eval_for_each(
                cast(ForEach, st), 
                input_data
            )
        elif st.statement == Statement.WHILE_STATEMEMT:
            return self.eval_while_statement(
                cast(While, st),
                input_data,
                evaluator_name
            )
        raise ValueError(f"Unexpected statement type!: {st.statement}")


    def eval_action(
        self, 
        action: Union[Action[Any, Any], Executor[Action[Any, Any]]],
        input_data: Transformable
    ) -> Transformable:
        """Evaluates an action statement."""
        # Update the register state based on the action
        return action(input_data)


    def eval_execute(
        self, 
        executable: Union[
            Executable[Input, Output], 
            Executor[Executable[Input, Output]]
        ],
        input_data: Transformable
    ) -> Transformable:
        """Evaluates an execute statement."""
        # Execute the executable and update the register accordingly
        return executable(input_data)
    
    
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
    

    def eval_delete_memory(
        self,
        delete_memory_command: DeleteMemory,
        input_data: Transformable
    ) -> Transformable:
        self.memory_manager.resolve_delete_memory(
            delete_memory_command
        )
        return input_data
    
    
    def eval_pipeline(
        self, 
        pipeline: ExecutionSchema,
        input_data: Transformable,
        evaluator_name: str
    ) -> Transformable:
        return self.eval_program(
            pipeline.retrieve_program(), 
            input_data,
            f"{evaluator_name}.{pipeline.__class__.__name__}"
        )

        
    def eval_condition(
        self, 
        condition: Union[Callable[[Transformable], bool], Condition],
        input_data: Transformable
    ) -> bool:
        if isinstance(condition, Condition):
            work_state = condition.get_state()
            if work_state != None:
                get_command = GetMemory(
                    work_state, MemoryGetInstruction.GET
                )
                input_data = self.memory_manager.resolve_get_memory(
                    get_command, input_data
                )
            ev = Evaluator(
                condition.get_statement(),
                cfg=EvaluatorConfigs(
                    name=f"{self.cfg.name}.{condition.__class__.__name__}",
                    logging_level=self.cfg.logging_level,
                    logging_handler=self.cfg.logging_handler,
                    fast_exit=self.cfg.fast_exit
                )
            )
            input_data = ev.eval_program(
                ev.program,
                copy.deepcopy(input_data),
                ev.cfg.name,
            )
            return condition.validator(input_data)
        elif callable(condition):
            return condition(copy.deepcopy(input_data))
        else:
            raise ValueError("Unsupported type of condition!")
    

    def eval_if_statement(
        self, 
        if_statement: IfStatement,
        input_data: Transformable,
        evaluator_name: str
    ) -> Transformable:
        bool_flag = self.eval_condition(
            condition=if_statement.get_condition(),
            input_data=input_data
        )
        
        if bool_flag == True:
            right_stetement = if_statement.get_right_statement()
            return self.eval(
                right_stetement, 
                input_data, 
                f"{evaluator_name}.{right_stetement.__class__.__name__}"
            )
        else:
            left_stetement = if_statement.get_left_statement()
            if left_stetement == None:
                return input_data
            return self.eval(
                left_stetement, 
                input_data,
                f"{evaluator_name}.{left_stetement.__class__.__name__}"
            )


    def eval_while_statement(
        self, 
        while_statement: While, 
        input_data: Transformable,
        evaluator_name: str
    ) -> Transformable:
        retries = while_statement.get_retries()
        if retries == None:
            while self.eval_condition(
                while_statement.get_condition(), 
                input_data
            ):
                input_data = self.eval(
                    while_statement.get_statement(),
                    input_data,
                    f"{evaluator_name}.{while_statement.__class__.__name__}"
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
                    input_data,
                    f"{evaluator_name}.{while_statement.__class__.__name__}"
                )
                retries -= 1
        return input_data


    def eval_filter_statement(
        self, filter_statement: Filter, input_data: Transformable
    ) -> Transformable:
        data = getattr(input_data, filter_statement.get_key)
        # need check that this is a sequence of dict

        setattr(
            input_data,
            filter_statement.set_key,
            [
                s for s in data
                if self.eval_condition(
                    filter_statement.get_condition(),
                    Transformable(s)
                )
            ]
        )
        return input_data

    
    def eval_for_each(
        self, for_each_statement: ForEach, input_data: Transformable
    ) -> Transformable:
        data = getattr(input_data, for_each_statement.get_key)
        # need check that this is a sequence of dict

        setattr(
            input_data,
            for_each_statement.set_key,
            [
                Evaluator(
                    for_each_statement.get_statement(),
                    cfg=EvaluatorConfigs(
                        name=f"{self.cfg.name}.{for_each_statement.__class__.__name__}",
                        logging_level=self.cfg.logging_level,
                        logging_handler=self.cfg.logging_handler,
                        fast_exit=self.cfg.fast_exit
                    )
                ).run_program(t)
                for t in data
            ]
        )
        return input_data