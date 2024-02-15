from __future__ import annotations
import json
from typing import (
    List, Any, Dict, Type, Iterator, Callable, TypeVar, Optional
)
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Config 
from core.executable_level_1.statements_types import Statement

T = TypeVar('T', bound='Serializable')

class Serializable:
    def to_json(self) -> str:
        """
        Serialize the object to a JSON string.
        """
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """
        Deserialize a JSON string to an object of the class.

        :param json_str: A JSON string representing the object.
        :return: An instance of the class with attributes set according to the JSON string.
        """
        attributes = json.loads(json_str)
        obj = cls()  
        obj.__dict__.update(attributes)
        return obj


class ExecutionSchema(Component):
    def __init__(self, cfg: Optional[Config]) -> None:
        super().__init__(cfg or Config())
        

class Pipeline(ExecutionSchema):
    stages: List[Component]

    def __init__(
        self, 
        cfg: Optional[Config]=None,
        *stage: Component
    ) -> None:
        self.stages = [*stage]
        super().__init__(cfg)
    

    def add(self, comp: Component) -> Pipeline:
        self.stages.append(comp)
        return self
    

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        state: Dict[str, Any] = input_data
        for stage in self.stages:
            state = stage.execute(state)
        return state
    

    def execute_batch(
        self, input_data: List[Dict[str, Any]]
    ) -> Iterator[Dict[str, Any]]:
        with ThreadPoolExecutor(max_workers=self.cfg.max_workers) as executor:
            return executor.map(
                self.execute, *input_data, timeout=self.cfg.timeout
            )


    def generate_statement(self) -> Dict[Statement, List[Dict[Statement, Any]]]:
        return {
            Statement.PIPELINE_STATEMENT: [
                st.generate_statement() for st in self.stages
            ]
        }


    def __or__(self, comp: Component) -> Pipeline:
        self.add(comp)
        return self


class Loop(ExecutionSchema):
    loop: Component
    condition: Callable[[Dict[str, Any], int], bool]

    def __init__(
        self, 
        cfg: Config,
        loop: Component,
        condition: Callable[[Dict[str, Any], int], bool]
    ) -> None:
        self.loop = loop
        self.condition = condition
        super().__init__(cfg)

    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        state: Dict[str, Any] = input_data
        count: int = 0

        while self.condition(state, count):
            state = self.loop.execute(state)
            count += 1
        
        return state
    

    def execute_batch(
        self, input_data: List[Dict[str, Any]]
    ) -> Iterator[Dict[str, Any]]:
        with ThreadPoolExecutor(max_workers=self.cfg.max_workers) as executor:
            return executor.map(
                self.execute, *input_data, timeout=self.cfg.timeout
            )


    def generate_statement(self) -> Dict[Statement, Any]:
        return {Statement.LOOP_STATEMENT: self.loop.generate_statement()}


class Path():
    condition: Callable[[Dict[str, Any]], bool] = lambda _: False
    executor: Component
    exit: bool = True


class Switch(ExecutionSchema):
    paths: List[Path]
    default: Path

    def __init__(self, cfg: Config, *path: Path, default: Path) -> None:
        self.paths = [*path]
        self.default = default
        super().__init__(cfg)

    
    def execute(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        states: List[Any] = []
        for path in self.paths:
            if not path.condition(input_data):
                continue
            state = path.executor.execute(input_data)
            if path.exit:
                return [state]
            states.append(state)
        
        states.append(self.default.executor.execute(input_data))
        return states
    

    def execute_batch(
        self, input_data: List[Dict[str, Any]]
    ) -> Iterator[List[Dict[str, Any]]]:
        with ThreadPoolExecutor(max_workers=self.cfg.max_workers) as executor:
            futures: List[Future[List[Dict[str, Any]]]] = [
                executor.submit(self.execute, i)
                for i in input_data
            ]
            for future in as_completed(futures, timeout=self.cfg.timeout):
                yield future.result()

    
    def generate_statement(self) -> Dict[Statement, Dict[str, Any]]:
        return {
            Statement.SWITCH_STATEMENT: dict((
                *(
                    (path.condition.__name__, path.executor.generate_statement()) 
                    for path in self.paths
                ),
                ('default', self.default.executor.generate_statement())
            )),
        }


class Parallel(ExecutionSchema):
    paths: List[Component]

    def __init__(self, cfg: Config, *path: Component) -> None:
        self.paths = [*path]
        super().__init__(cfg)

    
    def execute(self, input_data: Dict[str, Any]) -> Iterator[Any]:
        with ThreadPoolExecutor(max_workers=self.cfg.max_workers) as executor:
            futures: List[Future[Any]] = [
                executor.submit(path.execute, input_data)
                for path in self.paths
            ]
            for future in as_completed(futures):
                yield future.result()
            

    def execute_batch(
        self, input_data: List[Dict[str, Any]]
    ) -> List[Iterator[Any]]:
        states: List[Iterator[Any]] = []
        for i in input_data:
            states.append(self.execute(i))
        return states


    def generate_statement(self) -> Dict[Statement, List[Any]]:
        return {
            Statement.PARALLEL_STATEMENT: [
                path.generate_statement() for path in self.paths
            ]
        }


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









