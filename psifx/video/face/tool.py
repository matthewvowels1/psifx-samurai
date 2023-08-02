from typing import Union

from pathlib import Path

from psifx.video.tool import VideoTool


class FaceAnalysisTool(VideoTool):
    def inference(
        self,
        video_path: Union[str, Path],
        features_path: Union[str, Path],
    ):
        video_path = Path(video_path)
        features_path = Path(features_path)

        # video = load(video_path)
        # video = pre_process_func(video)
        # features = model(video)
        # features = post_process_func(features)
        # features.update({"metadata": metastuff})
        # write(features, features_path)

        raise NotImplementedError

    def visualization(
        self,
        video_path: Union[str, Path],
        features_path: Union[str, Path],
        visualization_path: Union[str, Path],
    ):
        raise NotImplementedError
