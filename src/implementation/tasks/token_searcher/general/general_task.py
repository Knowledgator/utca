from typing import Any, Union, Dict, cast

from implementation.tasks.token_searcher.base_token_searcher_task.base_token_searcher import (
    BaseTokenSearcher, 
    InputWithThreshold, 
    BaseTokenSearcherOutput, 
    BaseTokenSearcherConfig
)


class TokenSearcherGeneralInput(InputWithThreshold):
    prompt: str


class TokenSearcherGeneralOutput(BaseTokenSearcherOutput):
    prompt: str


class TokenSearcherGeneralConfig(BaseTokenSearcherConfig):
    pass


class TokenSearcherGeneralTask(BaseTokenSearcher):
    def _preprocess( # type: ignore ###############################################
        self, input_data: Union[TokenSearcherGeneralInput, Dict[str, Any]]
    ) -> TokenSearcherGeneralInput:

        return (
            input_data if isinstance(
                input_data, 
                TokenSearcherGeneralInput
            ) else TokenSearcherGeneralInput.parse_obj(input_data)
        )


    def _process(
        self, input_data: TokenSearcherGeneralInput
    ) -> Any:
        return self.get_predictions([input_data.prompt])
    

    def _postprocess(
        self, 
        input_data: TokenSearcherGeneralInput, 
        predicts: Any
    ) -> TokenSearcherGeneralOutput:
        return TokenSearcherGeneralOutput(
            prompt=input_data.prompt,
            output=[
                entity
                for output in predicts 
                for ent in output 
                if (entity:=self.build_entity(
                    input_data.prompt, ent, cast(float, input_data.threshold) ############
                ))
            ]
        )