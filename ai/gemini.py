from typing import Optional
import google.generativeai as genai
from ai.base_adapter import AIAdapter
from config import Config


class GeminiAdapter(AIAdapter):

    def __init__(
        self,
        system_instruction: Optional[str],
        api_key: str = Config.GEMINI_API_KEY,
        model: Optional[str] = Config.GEMINI_MODEL,
    ):
        self._api_key = api_key
        genai.configure(api_key=self._api_key)

        self._model = genai.GenerativeModel(
            model,
            system_instruction=system_instruction
        )

    def generate_content(self, message: str) -> str:
        response = self._model.generate_content(
            message,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
            )
        )

        return response.text
