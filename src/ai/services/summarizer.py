from src.ai.adapters.base import AIAdapter


class SummarizerService:
    """Service for summarizing weekly reports using AI models."""

    def __init__(self, adapter: AIAdapter):
        """
        Initialize the summarizer service with an AI adapter.

        Args:
            adapter: An implementation of AIAdapter
            to use for generating summaries
        """
        self.adapter = adapter

    def summarize(self, content: str) -> str:
        """
        Summarize the given content using the AI adapter.

        Args:
            content: The content to summarize

        Returns:
            A summary of the content
        """
        prompt = f"""
        Analise os seguintes relatórios diários e
        gere um resumo pequeno e simplificado:
        1. Atividades na semana
        2. Resolução de bugs
        3. Trabalhando em features

        Seja claro e direto, utilize pontos para destacar
        as principais informações importantes.
        Replique o formato de fala dos relatórios.

        Relatórios:

        {content}
        """

        return self.adapter.generate_content(prompt)
