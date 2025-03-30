import pytest
from unittest.mock import patch, MagicMock
from src.ai.adapters.gemini import GeminiAdapter


class TestGeminiAdapter:
    """Test suite for GeminiAdapter class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup fixtures for GeminiAdapter tests."""
        with patch("src.ai.adapters.gemini.genai") as mock_genai:
            mock_genai.GenerativeModel.return_value = MagicMock()
            self.mock_genai = mock_genai
            self.adapter = GeminiAdapter(
                system_instruction="Test instruction",
                api_key="test_key",
                model="test-model"
            )
            yield

    def test_gemini_adapter_initialization(self):
        """Test if GeminiAdapter is properly initialized."""
        assert self.adapter._api_key == "test_key"

        self.mock_genai.configure.assert_called_once_with(api_key="test_key")
        self.mock_genai.GenerativeModel.assert_called_once_with(
            "test-model", system_instruction="Test instruction"
        )

    def test_generate_content(self):
        """Test if generate_content method works correctly."""
        test_message = "Test message"
        expected_response = "Test response"

        mock_response = MagicMock()
        mock_response.text = expected_response
        self.adapter._model.generate_content.return_value = mock_response

        result = self.adapter.generate_content(test_message)

        self.adapter._model.generate_content.assert_called_once_with(
            test_message,
            generation_config=(
                self.adapter._model.generate_content.call_args[1]
                ["generation_config"]
            ),
        )
        assert result == expected_response
