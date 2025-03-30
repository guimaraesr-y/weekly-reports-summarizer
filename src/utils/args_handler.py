import argparse
from datetime import datetime
from typing import NamedTuple


class Args(NamedTuple):
    """Structure to hold parsed command line arguments."""

    reports_dir: str
    output_dir: str = None
    end_date: datetime = None
    format: str = "txt"
    verbose: bool = False


class ArgumentParser:
    """Class to handle command line argument parsing for Weekly Summarizer."""

    def __init__(self):
        """Initialize the argument parser with appropriate configuration."""
        self.parser = argparse.ArgumentParser(
            description=(
                "Weekly Reports Summarizer - "
                "Transform daily reports into concise weekly summaries"
            )
        )
        self._configure_arguments()

    def _configure_arguments(self):
        """Define the available command line arguments."""
        self.parser.add_argument(
            "-r",
            "--reports-dir",
            help=(
                "Directory containing daily report files "
                "(format: YYYY-MM-DD.md)"
            ),
            type=str,
            required=True,
        )

        self.parser.add_argument(
            "-o",
            "--output-dir",
            help=(
                "Directory for saving the generated summary "
                "(defaults to reports-dir if not specified)"
            ),
            type=str,
            required=False,
        )

        self.parser.add_argument(
            "-d",
            "--end-date",
            help=(
                "End date for the weekly summary (format: YYYY-MM-DD). "
                "Defaults to the most recent Sunday"
            ),
            type=str,
            required=False,
        )

        self.parser.add_argument(
            "-f",
            "--format",
            help="Output format for the summary (txt or md)",
            type=str,
            choices=["txt", "md"],
            default="txt",
            required=False,
        )

        self.parser.add_argument(
            "-v",
            "--verbose",
            help="Enable verbose output",
            action="store_true",
        )

    def parse(self) -> Args:
        """Parse command line arguments.

        Returns:
            Args: A named tuple containing the parsed arguments
        """
        args = self.parser.parse_args()

        end_date = None
        if args.end_date:
            try:
                end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
            except ValueError:
                self.parser.error("End date must be in the format YYYY-MM-DD")

        output_dir = args.output_dir if args.output_dir else args.reports_dir

        return Args(
            reports_dir=args.reports_dir,
            output_dir=output_dir,
            end_date=end_date,
            format=args.format,
            verbose=args.verbose,
        )
