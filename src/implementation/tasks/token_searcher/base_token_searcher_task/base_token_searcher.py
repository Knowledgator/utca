from typing import Type

from core.task_level_3.task import Task
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig, TokenSearcherModelInput, TokenSearcherModelOutput
)
from implementation.tasks.token_searcher.base_token_searcher_task.schema import (
    BaseTokenSearcherConfigType, InputWithThresholdType, BaseTokenSearcherOutputType
)

class BaseTokenSearcher(
    Task[
        BaseTokenSearcherConfigType, 
        InputWithThresholdType, 
        BaseTokenSearcherOutputType,
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
    ]
):
    input_class: Type[InputWithThresholdType]
    output_class: Type[BaseTokenSearcherOutputType]

    def choose_threshold(self, input_data: InputWithThresholdType):
        return (
            input_data.threshold 
            if not input_data.threshold is None 
            else self.cfg.threshold
        )
    

    def _preprocess(
        self, input_data: InputWithThresholdType
    ) -> InputWithThresholdType:
        input_data.threshold = self.choose_threshold(input_data)
        return input_data