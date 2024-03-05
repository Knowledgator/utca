from typing import Dict, Any, List, Optional, cast

from core.executable_level_1.schema import Transformable
from core.executable_level_1.eval import Condition, ExecutionSchema
from core.executable_level_1.actions import (
    ExecuteFunctionOneToOne,
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
        subject_key: str
    ) -> None:
        if semantic_schema is None:
            semantic_schema = SemanticSearchSchema()
        self.semantic_schema = semantic_schema
        super().__init__(
            self.validator_wrapper(distance), 
            self.build_statement(subject_key, targets, self.semantic_schema),
            None
        )

    
    def build_statement(
        self, 
        subject_key: str,
        targets: List[str],
        semantic_schema: SemanticSearchSchema
    ) -> ExecutionSchema:
        def build_dataset(input_data: Dict[str, Any]) -> Dict[str, Any]:
            semantic_schema.add([input_data[subject_key]])
            return input_data

        return (
            ExecuteFunctionOneToOne(build_dataset)
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
                cast(
                    Dict[str, Any],
                    input_data.extract()
                )["search_results"]["distances"]
            )
        return validator
    

    def get_statement(self) -> ExecutionSchema:
        self.semantic_schema.drop_index()
        return self.statement