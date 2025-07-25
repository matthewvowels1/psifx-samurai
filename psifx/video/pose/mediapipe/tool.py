"""MediaPipe pose estimation tool."""

from typing import Any, Dict, List, Tuple, Union

import json
from pathlib import Path
from tqdm import tqdm

import numpy as np
from mediapipe.python.solutions.holistic import Holistic

from psifx.video.pose.tool import PoseEstimationTool
from psifx.video.pose.mediapipe import skeleton
from psifx.io import tar, video


class MediaPipePoseEstimationTool(PoseEstimationTool):
    """
    MediaPipe pose estimation tool.

    :param model_complexity: Complexity of the model: {0, 1, 2}, higher means more FLOPs, but also more accurate results
    :param smooth: Whether to temporally smooth the inference results to reduce the jitter.
    :param device: The device where the computation should be executed.
    :param overwrite: Whether to overwrite existing files, otherwise raise an error.
    :param verbose: Whether to execute the computation verbosely.
    """

    def __init__(
        self,
        model_complexity: int = 2,
        smooth: bool = True,
        device: str = "cpu",
        overwrite: bool = False,
        verbose: Union[bool, int] = True,
    ):
        super().__init__(
            device=device,
            overwrite=overwrite,
            verbose=verbose,
        )

        if self.device != "cpu":
            print("Only CPU support is currently available for MediaPipe pose estimation tool.")
        self.model_complexity = model_complexity
        self.smooth = smooth

    def process_part(
        self,
        landmarks,
        size: Tuple[int, int],
        n_points: int,
    ) -> List[float]:
        """
        Processes MediaPipe output into a simple flattened list of coordinates.

        :param landmarks: MediaPipe landmarks.
        :param size: Image resolution.
        :param n_points: Expected number of points.
        :return: Processed keypoint coordinates.
        """
        h, w = size
        if landmarks is not None:
            landmarks = [[p.x, p.y, p.visibility] for p in landmarks.landmark]
            points = np.array(landmarks, dtype=np.float32)
            points[:, 0] *= w - 1
            points[:, 1] *= h - 1
        else:
            points = np.zeros((n_points, 3), dtype=np.float32)
        return points.flatten().tolist()

    def process_pose(
        self,
        results,
        size: Tuple[int, int],
    ) -> Dict[str, Any]:
        """
        Process all the parts estimated by MediaPipe, e.g. body, face, hands.

        :param results: MediaPipe output.
        :param size: Image resolution.
        :return: Processed keypoints for every part.
        """
        return {
            "pose_keypoints_2d": self.process_part(
                landmarks=results.pose_landmarks,
                size=size,
                n_points=skeleton.N_POSE_LANDMARKS,
            ),
            "face_keypoints_2d": self.process_part(
                landmarks=results.face_landmarks,
                size=size,
                n_points=skeleton.N_FACE_LANDMARKS,
            ),
            "hand_left_keypoints_2d": self.process_part(
                landmarks=results.left_hand_landmarks,
                size=size,
                n_points=skeleton.N_LEFT_HAND_LANDMARKS,
            ),
            "hand_right_keypoints_2d": self.process_part(
                landmarks=results.right_hand_landmarks,
                size=size,
                n_points=skeleton.N_LEFT_HAND_LANDMARKS,
            ),
        }

    def inference(
        self,
        video_path: Union[str, Path],
        poses_path: Union[str, Path],
    ):
        """
        Runs MediaPipe pose estimation model on a video.

        :param video_path: Path to the video file.
        :param poses_path: Path to the pose archive.
        :return:
        """
        video_path = Path(video_path)
        poses_path = Path(poses_path)

        if self.verbose:
            print(f"video   =   {video_path}")
            print(f"poses   =   {poses_path}")

        tar.TarWriter.check(path=poses_path, overwrite=self.overwrite)

        poses = {
            "edges": {
                "pose_keypoints_2d": skeleton.POSE_EDGES,
                "face_keypoints_2d": skeleton.FACE_EDGES,
                "hand_left_keypoints_2d": skeleton.LEFT_HAND_EDGES,
                "hand_right_keypoints_2d": skeleton.RIGHT_HAND_EDGES,
            }
        }

        # We have to instantiate the model for every call, because of internal states.
        # Not that it is very costly anyway.
        with (
            Holistic(
                static_image_mode=False,
                model_complexity=self.model_complexity,
                smooth_landmarks=self.smooth,
                enable_segmentation=False,
                smooth_segmentation=False,
                refine_face_landmarks=True,
            ) as model,
            video.VideoReader(path=video_path) as video_reader,
        ):
            for i, image in enumerate(
                tqdm(
                    video_reader,
                    desc="Processing",
                    disable=not self.verbose,
                )
            ):
                h, w, _ = image.shape
                results = model.process(image)
                poses[f"{i: 015d}"] = self.process_pose(
                    results=results,
                    size=(h, w),
                )

        poses = {
            f"{k}.json": json.dumps(v)
            for k, v in tqdm(
                poses.items(),
                desc="Encoding",
                disable=not self.verbose,
            )
        }
        tar.TarWriter.write(
            dictionary=poses,
            path=poses_path,
            overwrite=self.overwrite,
            verbose=self.verbose,
        )
