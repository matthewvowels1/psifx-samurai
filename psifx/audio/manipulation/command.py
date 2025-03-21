"""audio manipulation command-line interface."""

import argparse
from pathlib import Path

from psifx.utils.command import Command, register_command
from psifx.audio.manipulation.tool import ManipulationTool


class ManipulationCommand(Command):
    """
    Command-line interface for manipulating audio tracks.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        subparsers = parser.add_subparsers(title="available commands")

        register_command(subparsers, "extraction", ExtractionCommand)
        register_command(subparsers, "conversion", ConversionCommand)
        register_command(subparsers, "split", SplitCommand)
        register_command(subparsers, "mixdown", MixDownCommand)
        register_command(subparsers, "normalization", NormalizationCommand)
        register_command(subparsers, "trim", TrimCommand)

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        parser.print_help()


class ExtractionCommand(Command):
    """
    Command-line interface for extracting the audio track from a video.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        parser.add_argument(
            "--video",
            type=Path,
            required=True,
            help="path to the input video file, such as ``/path/to/video.mp4`` (or .avi, .mkv, etc.)",
        )
        parser.add_argument(
            "--audio",
            type=Path,
            required=True,
            help="path to the output audio file, such as ``/path/to/audio.wav``",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="overwrite existing files, otherwise raises an error",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="verbosity of the script",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        tool = ManipulationTool(
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
        tool.extraction(
            video_path=args.video,
            audio_path=args.audio,
        )
        del tool


class ConversionCommand(Command):
    """
    Command-line interface for converting any audio track to a mono audio track at 16kHz sample rate.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        parser.add_argument(
            "--audio",
            type=Path,
            required=True,
            help="path to the input audio file, such as ``/path/to/audio.wav`` (or .mp3, etc.)",
        )
        parser.add_argument(
            "--mono_audio",
            type=Path,
            required=True,
            help="path to the output audio file, such as ``/path/to/mono-audio.wav``",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="overwrite existing files, otherwise raises an error",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="verbosity of the script",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        tool = ManipulationTool(
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
        tool.convert(
            audio_path=args.audio,
            mono_audio_path=args.mono_audio,
        )
        del tool



class SplitCommand(Command):
    """
    Command-line interface for splitting a stereo audio track into two mono tracks.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        parser.add_argument(
            "--stereo_audio",
            type=Path,
            required=True,
            help="path to the input stereo audio file, such as ``/path/to/stereo-audio.wav``",
        )
        parser.add_argument(
            "--left_audio",
            type=Path,
            required=True,
            help="path to the output left channel mono audio file, such as ``/path/to/left-audio.wav``",
        )
        parser.add_argument(
            "--right_audio",
            type=Path,
            required=True,
            help="path to the output right channel mono audio file, such as ``/path/to/right-audio.wav``",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="overwrite existing files, otherwise raises an error",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="verbosity of the script",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        tool = ManipulationTool(
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
        tool.split(
            stereo_audio_path=args.stereo_audio,
            left_audio_path=args.left_audio,
            right_audio_path=args.right_audio,
        )
        del tool


class MixDownCommand(Command):
    """
    Command-line interface for mixing multiple mono audio tracks.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        parser.add_argument(
            "--mono_audios",
            nargs="+",
            type=Path,
            required=True,
            help="paths to the input mono audio files, such as ``/path/to/mono-audio-1.wav /path/to/mono-audio-2.wav``",
        )
        parser.add_argument(
            "--mixed_audio",
            type=Path,
            required=True,
            help="path to the output mixed audio file, such as ``/path/to/mixed-audio.wav``",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="overwrite existing files, otherwise raises an error",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="verbosity of the script",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        tool = ManipulationTool(
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
        tool.mixdown(
            mono_audio_paths=args.mono_audios,
            mixed_audio_path=args.mixed_audio,
        )
        del tool


class NormalizationCommand(Command):
    """
    Command-line interface for normalizing an audio track.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        parser.add_argument(
            "--audio",
            type=Path,
            required=True,
            help="path to the input audio file, such as ``/path/to/audio.wav``",
        )
        parser.add_argument(
            "--normalized_audio",
            type=Path,
            required=True,
            help="path to the output normalized audio file, such as ``/path/to/normalized-audio.wav``",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="overwrite existing files, otherwise raises an error",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="verbosity of the script",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        tool = ManipulationTool(
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
        tool.normalization(
            audio_path=args.audio,
            normalized_audio_path=args.normalized_audio,
        )
        del tool



class TrimCommand(Command):
    """
    Command-line interface for trimming an audio track.
    """

    @staticmethod
    def setup(parser: argparse.ArgumentParser):
        """
        Sets up the command.

        :param parser: The argument parser.
        :return:
        """
        parser.add_argument(
            "--audio",
            type=Path,
            required=True,
            help="path to the input audio file, such as ``/path/to/audio.wav``",
        )
        parser.add_argument(
            "--trimmed_audio",
            type=Path,
            required=True,
            help="path to the output trimmed audio file, such as ``/path/to/trimmed-audio.wav``",
        )
        parser.add_argument(
            "--start_time",
            type=float,
            default=None,
            help="start time in seconds (None to keep from beginning)",
        )
        parser.add_argument(
            "--end_time",
            type=float,
            default=None,
            help="end time in seconds (None to keep until end)",
        )
        parser.add_argument(
            "--overwrite",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="overwrite existing files, otherwise raises an error",
        )
        parser.add_argument(
            "--verbose",
            default=True,
            action=argparse.BooleanOptionalAction,
            help="verbosity of the script",
        )

    @staticmethod
    def execute(parser: argparse.ArgumentParser, args: argparse.Namespace):
        """
        Executes the command.

        :param parser: The argument parser.
        :param args: The arguments.
        :return:
        """
        tool = ManipulationTool(
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
        tool.trim(
            audio_path=args.audio,
            trimmed_audio_path=args.trimmed_audio,
            start_time=args.start_time,
            end_time=args.end_time,
        )
        del tool