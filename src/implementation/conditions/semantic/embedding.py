from typing import Dict, Any, List, Optional

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import Transformable
from core.executable_level_1.eval import Condition, ExecutionSchema
from core.executable_level_1.actions import (
    ExecuteFunction,
    AddData
)
from implementation.schemas.semantic_search_schema import (
    SemanticSearchSchema
)

class SemanticCondition(Condition):
    def __init__(
        self,
        *,
        distance: float,
        targets: List[str],
        semantic_schema: Optional[SemanticSearchSchema]=None,
        subject_key: str,
        name: Optional[str]=None
    ) -> None:
        if semantic_schema is None:
            semantic_schema = SemanticSearchSchema()
        self.semantic_schema = semantic_schema
        super().__init__(
            self.validator_wrapper(distance), 
            self.build_schema(subject_key, targets, self.semantic_schema),
            None,
            name
        )

    
    def build_schema(
        self, 
        subject_key: str,
        targets: List[str],
        semantic_schema: SemanticSearchSchema
    ) -> ExecutionSchema:
        def build_index(input_data: Dict[str, Any]) -> Dict[str, Any]:
            semantic_schema.add([input_data[subject_key]])
            return input_data

        return (
            ExecuteFunction(build_index)
            | AddData({
                "query": targets,
                "results_count": 1
            })
            | semantic_schema
        )

    
    @classmethod
    def validator_wrapper(cls, distance: float):
        def validator(input_data: Transformable) -> bool:
            return any(
                res_distance[0] <= distance
                for res_distance in
                input_data.extract()["search_results"]["distances"]
            )
        return validator
    

    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> bool:
        self.semantic_schema.drop_index()
        return super()(input_data, evaluator)