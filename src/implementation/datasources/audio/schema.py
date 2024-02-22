from typing import List, Any

from core.datasource_level_2.schema import (
    DatasourceInput, DatasourceOutput
)

class AudioReadInput(DatasourceInput):
    path_to_file: str


class AudioReadOutput(DatasourceOutput):
    audio_data: List[Any]
    sample_rate: int


class AudioWriteInput(DatasourceInput):
    path_to_file: str
    audio_data: List[Any]
    sampling_rate: int


class AudioWriteOutput(DatasourceOutput):
    ...