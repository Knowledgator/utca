from typing import Dict, Any

import cv2

from core.executable_level_1.actions import Action

class VideoRead(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        video = cv2.VideoCapture(input_data["path_to_file"])
        # video.release() TODO: need to be called?
        input_data["video_data"] = video
        return input_data


class VideoWrite(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        w = cv2.VideoWriter(
            input_data["path_to_file"],
            cv2.VideoWriter_fourcc(*input_data["fourcc"]), # type: ignore
            input_data["fps"], 
            (input_data["width"], input_data["height"])
        )
        for frame in input_data["frames"]:
            w.write(frame)
        w.release()
        return {}


class VideoReleaseCapture(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        video = input_data.pop("video_data")
        video.release()
        return input_data


