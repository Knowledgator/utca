from typing import Dict, Any, List, Optional

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.schema import Transformable
from utca.core.executable_level_1.eval import Condition, ExecutionSchema
from utca.core.executable_level_1.actions import (
    ExecuteFunction,
    AddData
)
from utca.implementation.schemas.semantic_search.semantic_search_schema import (
    SemanticSearchSchema
)

class SemanticCondition(Condition):
    """
    Semantic condition
    """
    def __init__(
        self,
        *,
        distance: float,
        targets: List[str],
        semantic_schema: Optional[SemanticSearchSchema]=None,
        subject_key: str,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            distance (float): Distance thresholde.
            
            targets (List[str]): Comparison targets.
            
            subject_key (str): Key associated with source of subjects to match.
                Source should be a list of strings.
            
            semantic_schema (Optional[SemanticSearchSchema], optional): Schema that will be used
                for distance evaluation. If equals to None, default SemanticSearchSchema
                will be used. Defaults to None.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
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
        """
        Builds evaluation schema

        Args:
            subject_key (str): Key associated with source of subjects to match.
                Source should be a list of strings.

            targets (List[str]): Comparison targets.
            
            semantic_schema (SemanticSearchSchema): Schema that will be used
                for distance evaluation.

        Returns:
            ExecutionSchema: Schema for distance evaluation.
        """
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
        """
        Create validator for Condition

        Args:
            distance (float): Distance thresholde.
        """
        def validator(input_data: Transformable, evaluator: Evaluator) -> bool:
            """
            Validator for condition

            Args:
                input_data (Transformable): Data to process.

                evaluator (Evaluator): Evaluator in context of wich executed.

            Returns:
                bool: Result of evaluation. Define that condition is fulfilled or not.
            """
            return any(
                res_distance[0] <= distance
                for res_distance in
                input_data.extract()["search_results"]["distances"]
            )
        return validator
    

    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> bool:
        """
        Args:
            input_data (Transformable): Data for processing
            
            evaluator (Evaluator): Evaluator in context of wich Condition executed.

        Returns:
            bool: Result of evaluation. Define that condition is fulfilled or not.
        """
        self.semantic_schema.drop_index()
        return super().__call__(input_data, evaluator)