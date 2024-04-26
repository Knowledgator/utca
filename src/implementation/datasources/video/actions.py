from typing import Dict, Any

import cv2

from core.executable_level_1.actions import Action

class VideoRead(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Read video file
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to video file;

        Returns:
            Dict[str, Any]: Expected keys:
                'video' (cv2.VideoCapture): Video;
        """
        video = cv2.VideoCapture(input_data["path_to_file"])
        return {
            "video": video
        }


class VideoWrite(Action[Dict[str, Any], None]):
    """
    Write video frame by frame to file
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to plain text file;

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


class VideoReleaseCapture(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Release video capture
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'video' (cv2.VideoCapture): Video capture to release;

        Returns:
            Dict[str, Any]: Input data without video key;
        """
        video = input_data.pop("video")
        video.release()
        return input_data