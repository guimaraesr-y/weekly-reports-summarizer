import pytest
from datetime import datetime
from src.utils.args_handler import ArgumentParser


class TestArgumentParser:
    """Test suite for ArgumentParser class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup fixture that provides an ArgumentParser instance."""
        self.parser = ArgumentParser()

    def test_parse_required_args(self):
        """Test parsing of required arguments."""
        test_args = ["--reports-dir", "test_dir"]

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("sys.argv", ["script.py"] + test_args)
            args = self.parser.parse()

            assert args.reports_dir == "test_dir"
            assert args.output_dir == "test_dir"
            assert args.end_date is None
            assert args.format == "txt"
            assert args.verbose is False

    def test_parse_all_args(self):
        """Test parsing of all arguments."""
        test_args = [
            "--reports-dir", "test_dir",
            "--output-dir", "output_dir",
            "--end-date", "2024-03-28",
            "--format", "md",
            "--verbose"
        ]

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("sys.argv", ["script.py"] + test_args)
            args = self.parser.parse()

            assert args.reports_dir == "test_dir"
            assert args.output_dir == "output_dir"
            assert args.end_date == datetime(2024, 3, 28)
            assert args.format == "md"
            assert args.verbose is True

    def test_invalid_end_date(self):
        """Test handling of invalid end date format."""
        test_args = [
            "--reports-dir", "test_dir",
            "--end-date", "invalid-date"
        ]

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("sys.argv", ["script.py"] + test_args)
            with pytest.raises(SystemExit):
                self.parser.parse()

    def test_invalid_format(self):
        """Test handling of invalid format option."""
        test_args = [
            "--reports-dir", "test_dir",
            "--format", "invalid"
        ]

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("sys.argv", ["script.py"] + test_args)
            with pytest.raises(SystemExit):
                self.parser.parse()

    def test_missing_required_args(self):
        """Test handling of missing required arguments."""
        test_args = []

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("sys.argv", ["script.py"] + test_args)
            with pytest.raises(SystemExit):
                self.parser.parse()
