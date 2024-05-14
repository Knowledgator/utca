from typing import Dict, Any, Optional

import cv2

from utca.core.executable_level_1.actions import Action

class VideoRead(Action[Dict[str, Any], cv2.VideoCapture]):
    """
    Read video file
    """
    def __init__(
        self,
        name: Optional[str]=None,
        default_key: str="video",
    ) -> None:
        """
        Args:
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        super().__init__(name=name, default_key=default_key)
    

    def execute(self, input_data: Dict[str, Any]) -> cv2.VideoCapture:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to video file;

        Returns:
            cv2.VideoCapture: Video;
        """
        return cv2.VideoCapture(input_data["path_to_file"])


class VideoWrite(Action[Dict[str, Any], None]):
    """
    Write video frame by frame to file
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to video file;

                'fourcc' (str): Codec to use;

                'fps' (int): FPS to use;

                'width' (int): Frame width to use in pixels;

                'height' (int): Frame height to use in pixels;

                'frames' (ndarray): Frames to write;
        Raises:
            Exception: If unable to write file.
        """
        try:
            w = cv2.VideoWriter(
                input_data["path_to_file"],
                cv2.VideoWriter_fourcc(*input_data["fourcc"]), # type: ignore
                input_data["fps"], 
                (input_data["width"], input_data["height"])
            )
            for frame in input_data["frames"]:
                w.write(frame)
            w.release()
        except Exception as e:
            raise Exception(f"Unable to write file: {e}")


class VideoReleaseCapture(Action[cv2.VideoCapture, None]):
    """
    Release video capture
    """
    def execute(self, input_data: cv2.VideoCapture) -> None:
        """
        Args:
            input_data (cv2.VideoCapture): Video capture to release;
        """
        input_data.release()