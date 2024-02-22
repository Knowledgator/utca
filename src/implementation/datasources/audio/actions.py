from typing import Type, Dict, Any

import numpy as np

from core.datasource_level_2.schema import DatasourceConfig
from core.datasource_level_2.datasource import DatasourceAction
from implementation.datasources.audio.schema import (
    AudioReadInput,
    AudioReadOutput,
    AudioWriteInput,
    AudioWriteOutput
)

class AudioRead(DatasourceAction[
    DatasourceConfig,
    AudioReadInput,
    AudioReadOutput
]):
    input_class: Type[AudioReadInput] = AudioReadInput
    output_class: Type[AudioReadOutput] = AudioReadOutput

    def invoke(self, input_data: AudioReadInput) -> Dict[str, Any]:
        audio_data, samplerate = sf.read(input_data.path_to_file) # type: ignore 
        return {
            'audio_data': audio_data,
            'sample_rate': samplerate
        }


    def invoke_batch(self, input_data: list[AudioReadInput]) -> list[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]


class AudioWrite(DatasourceAction[
    DatasourceConfig,
    AudioWriteInput,
    AudioWriteOutput
]):
    input_class: Type[AudioWriteInput] = AudioWriteInput 
    output_class: Type[AudioWriteOutput] = AudioWriteOutput

    def invoke(self, input_data: AudioWriteInput) -> Dict[str, Any]:
        sf.write( # type: ignore
            input_data.path_to_file, 
            np.ravel(input_data.audio_data),
            input_data.sampling_rate
        )
        return {}


    def invoke_batch(self, input_data: list[AudioWriteInput]) -> list[Dict[str, Any]]:
        for i in input_data:
            self.invoke(i)
        return []