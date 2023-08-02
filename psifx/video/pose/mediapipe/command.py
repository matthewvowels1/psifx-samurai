import argparse
from pathlib import Path

from psifx.command import Command, register_command
from psifx.video.pose.mediapipe.tool import (
    MediaPipePoseEstimationTool,
    MediaPipePoseEstimationAndSegmentationTool,
)


class MediaPipeCommand(Command):
    """
    Tool for running MediaPipe.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(title="available commands")

        from psifx.video.pose.command import VisualizationCommand

        register_command(subparsers, "inference", MediaPipeInferenceCommand)
        register_command(subparsers, "visualization", VisualizationCommand)

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        parser.print_help()


class MediaPipeInferenceCommand(Command):
    """
    Tool for inferring human pose with MediaPipe Holistic.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        parser.add_argument(
            "--video",
            type=Path,
            required=True,
        )
        parser.add_argument(
            "--poses",
            type=Path,
            required=True,
        )
        parser.add_argument(
            "--masks",
            type=Path,
            default=None,
        )
        parser.add_argument(
            "--mask_threshold",
            type=float,
            default=0.1,
        )
        parser.add_argument(
            "--model_complexity",
            type=int,
            default=2,
            help="Complexity of the model, either 0, 1 or 2. Higher means more FLOPs, but also more accurate results.",
        )
        parser.add_argument(
            "--smooth",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="Whether to temporally smooth the inference results to reduce the jitter.",
        )
        parser.add_argument(
            "--device",
            type=str,
            default="cpu",
            help="Device on which to run the inference, either 'cpu' or 'cuda'.",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="Overwrite existing files, otherwise raises an error.",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="Verbosity of the script.",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        if args.masks is None:
            tool = MediaPipePoseEstimationTool(
                model_complexity=args.model_complexity,
                smooth=args.smooth,
                device=args.device,
                overwrite=args.overwrite,
                verbose=args.verbose,
            )
            tool.inference(
                video_path=args.video,
                poses_path=args.poses,
            )
        else:
            tool = MediaPipePoseEstimationAndSegmentationTool(
                model_complexity=args.model_complexity,
                smooth=args.smooth,
                mask_threshold=args.mask_threshold,
                device=args.device,
                overwrite=args.overwrite,
                verbose=args.verbose,
            )
            tool.inference(
                video_path=args.video,
                poses_path=args.poses,
                masks_path=args.masks,
            )
        del tool
