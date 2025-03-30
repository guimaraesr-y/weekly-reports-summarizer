from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from freezegun import freeze_time
import pytest
from src.ai.services.summarizer import WeeklySummarizer
from src.ai.adapters.base import AIAdapter


class TestWeeklySummarizer:
    """Test suite for WeeklySummarizer class."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Setup fixtures for WeeklySummarizer tests."""
        # Create a temporary directory for test reports
        self.reports_dir = tmp_path / "reports"
        self.reports_dir.mkdir()

        # Create mock AI adapter
        self.mock_ai = MagicMock(spec=AIAdapter)
        self.mock_ai.generate_content.return_value = "Test summary"

        # Create summarizer instance
        self.summarizer = WeeklySummarizer(
            reports_directory=str(self.reports_dir),
            ai=self.mock_ai
        )

    def test_initialization(self):
        """Test if WeeklySummarizer is properly initialized."""
        assert self.summarizer.reports_directory == str(self.reports_dir)
        assert self.summarizer._ai == self.mock_ai

    @freeze_time("2025-03-25")
    def test_get_last_week_start(self):
        """Test _get_last_week_start method."""
        last_week_start = datetime.strptime("2025-03-16", "%Y-%m-%d")
        assert self.summarizer._get_last_week_start() == last_week_start

    @freeze_time("2025-03-25")
    def test_get_last_week_end(self):
        """Test _get_last_week_end method."""
        last_week_end = datetime.strptime("2025-03-22", "%Y-%m-%d")
        assert self.summarizer._get_last_week_end() == last_week_end

    def test_get_weekly_reports_empty_directory(self):
        """Test _get_weekly_reports with empty directory."""
        start_date = datetime(2024, 3, 7)
        end_date = datetime(2024, 3, 14)  # Friday
        reports = self.summarizer._get_weekly_reports(start_date, end_date)
        assert reports == ""

    def test_get_weekly_reports_with_files(self):
        """Test _get_weekly_reports with existing report files."""
        # Create test report files
        last_week = datetime.now() - timedelta(days=7)

        start_date = last_week - timedelta(days=last_week.weekday())
        end_date = start_date + timedelta(days=5)

        for i in range(5):
            date = start_date + timedelta(days=i)
            report_file = self.reports_dir / f"{date.strftime('%Y-%m-%d')}.md"
            report_file.write_text(f"Report for {date.strftime('%Y-%m-%d')}")

        reports = self.summarizer._get_weekly_reports(start_date, end_date)
        assert len(reports.split("\n\n")) == 5  # Should have 5 reports

    def test_get_weekly_reports_with_missing_files(self):
        """Test _get_weekly_reports with some missing files."""
        end_date = datetime(2024, 3, 14)  # Friday
        start_date = end_date - timedelta(days=5)  # Sunday

        # Create only some report files
        dates_to_create = [start_date, start_date + timedelta(days=2),
                           start_date + timedelta(days=4), end_date]

        for date in dates_to_create:
            report_file = self.reports_dir / f"{date.strftime('%Y-%m-%d')}.md"
            report_file.write_text(f"Report for {date.strftime('%Y-%m-%d')}")

        reports = self.summarizer._get_weekly_reports(start_date, end_date)
        assert len(reports.split("\n\n")) == 4  # Should have 4 reports

    def test_generate_weekly_summary_with_end_date(self):
        """Test generate_weekly_summary with specific end date."""
        end_date = datetime(2024, 3, 15)  # Friday

        # Create test report files
        start_date = end_date - timedelta(days=6)
        for i in range(7):
            date = start_date + timedelta(days=i)
            report_file = self.reports_dir / f"{date.strftime('%Y-%m-%d')}.md"
            report_file.write_text(f"Report for {date.strftime('%Y-%m-%d')}")

        summary = self.summarizer.generate_weekly_summary(end_date)

        # Verify AI was called with correct prompt
        self.mock_ai.generate_content.assert_called_once()
        call_args = self.mock_ai.generate_content.call_args[0][0]
        assert "Relatórios:" in call_args
        assert "Test summary" == summary

    def test_generate_weekly_summary_default_end_date(self):
        """Test generate_weekly_summary with default end date."""
        today = datetime.now()
        expected_end_date = today - timedelta(days=today.weekday())

        # Create test report files
        start_date = expected_end_date - timedelta(days=6)
        for i in range(7):
            date = start_date + timedelta(days=i)
            report_file = self.reports_dir / f"{date.strftime('%Y-%m-%d')}.md"
            report_file.write_text(f"Report for {date.strftime('%Y-%m-%d')}")

        summary = self.summarizer.generate_weekly_summary()

        # Verify AI was called with correct prompt
        self.mock_ai.generate_content.assert_called_once()
        call_args = self.mock_ai.generate_content.call_args[0][0]
        assert "Relatórios:" in call_args
        assert "Test summary" == summary

    @patch("src.config.settings.Config.DEBUG", True)
    def test_generate_weekly_summary_with_debug(self):
        """Test generate_weekly_summary with debug mode enabled."""
        end_date = datetime(2024, 3, 15)

        # Create test report file
        report_file = self.reports_dir / f"{end_date.strftime('%Y-%m-%d')}.md"
        report_file.write_text("Test report content")

        with patch("builtins.print") as mock_print:
            self.summarizer.generate_weekly_summary(end_date)
            mock_print.assert_called_once()
            assert "[DEBUG] PROMPT:" in mock_print.call_args[0][0]
