from typing import Dict, Any, Type, Optional, Union

import cv2

from core.datasource_level_2.datasource import DatasourceManager, DatasourceAction
from core.datasource_level_2.schema import (
    DatasourceConfig,
    DatasourceInput,
    DatasourceOutput
)

class VideoReadInput(DatasourceInput):
    path_to_file: str


class VideoReadOutput(DatasourceOutput):
    

    def __init__(self, *, video_data: cv2.VideoCapture):
        self.video_data = video_data


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


    def model_dump(
        self, 
        *, 
        mode: str='python', 
        include: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        exclude: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        by_alias: bool=False, 
        exclude_unset: bool=False,
        exclude_defaults: bool=False,
        exclude_none: bool=False, 
        round_trip: bool=False,
        warnings: bool=True
    ) -> Dict[str, Any]:
        return {'video_data': self.video_data}


class VideoRead(DatasourceAction[
    DatasourceConfig,
    VideoReadInput,
    VideoReadOutput
]):
    input_class: Type[VideoReadInput] = VideoReadInput
    output_class: Type[VideoReadOutput] = VideoReadOutput

    def invoke(self, input_data: VideoReadInput) -> Dict[str, Any]:
        video = cv2.VideoCapture(input_data.path_to_file)
        # video.release() TODO: need to be called?
        return {
            'video_data': video
        }


    def invoke_batch(self, input_data: list[VideoReadInput]) -> list[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]


class VideoWriteInput(DatasourceInput):
    path_to_file: str
    frames: Any
    width: int
    height: int
    fourcc: str # https://fourcc.org/codecs.php
    fps: float


class VideoWriteOutput(DatasourceOutput):
    ...


class VideoWrite(DatasourceAction[
    DatasourceConfig,
    VideoWriteInput,
    VideoWriteOutput
]):
    input_class: Type[VideoWriteInput] = VideoWriteInput 
    output_class: Type[VideoWriteOutput] = VideoWriteOutput

    def invoke(self, input_data: VideoWriteInput) -> Dict[str, Any]:
        w = cv2.VideoWriter(
            input_data.path_to_file,
            cv2.VideoWriter_fourcc(*input_data.fourcc), # type: ignore
            input_data.fps, 
            (input_data.width, input_data.height)
        )
        for frame in input_data.frames:
            w.write(frame)
        w.release()
        return {}


    def invoke_batch(self, input_data: list[VideoWriteInput]) -> list[Dict[str, Any]]:
        for i in input_data:
            self.invoke(i)
        return []


class Video(DatasourceManager[
    DatasourceConfig,
    VideoReadInput,
    VideoReadOutput,

    DatasourceConfig,
    VideoWriteInput,
    VideoWriteOutput,
]):
    def read(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> VideoRead:
        return VideoRead(cfg)

    
    def write(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> VideoWrite:
        return VideoWrite(cfg)


