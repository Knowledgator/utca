from typing import Any, Union, Dict, Type

from implementation.models.token_searcher.model import (
    BaseTokenSearcherModel
)
from implementation.tasks.token_searcher.base_token_searcher_task.schema import (
    BaseTokenSearcherConfigType, InputWithThresholdType, BaseTokenSearcherOutputType
)

class BaseTokenSearcher(
    BaseTokenSearcherModel[
        BaseTokenSearcherConfigType, 
        InputWithThresholdType, 
        BaseTokenSearcherOutputType
    ]
):
    input_data_type: Type[InputWithThresholdType]

    def __init__(self, cfg: BaseTokenSearcherConfigType) -> None:
        super().__init__(cfg)


    def choose_threshold(self, input_data: InputWithThresholdType):
        return (
            input_data.threshold 
            if not input_data.threshold is None 
            else self.cfg.threshold
        )
    

    def _preprocess(
        self, input_data: Union[InputWithThresholdType, Dict[str, Any]]
    ) -> InputWithThresholdType:
        input_data = super()._preprocess(input_data)
        input_data.threshold = self.choose_threshold(input_data)
        return input_data