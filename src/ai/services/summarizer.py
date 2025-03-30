import os
from datetime import datetime, timedelta

from src.ai.adapters.base import AIAdapter
from src.config.settings import Config


class WeeklySummarizer:

    __slots__ = ["reports_directory", "_ai"]

    def __init__(self, reports_directory, ai: AIAdapter = None):
        self.reports_directory = reports_directory
        self._ai = ai

    def _get_weekly_reports(self, end_date):
        """
        Coleta todos os relatórios de uma semana específica.
        Formato dos arquivos: YYYY-MM-DD.md em uma única pasta.
        """
        start_date = end_date - timedelta(days=7)
        weekly_reports = []

        date_range = [start_date + timedelta(days=x) for x in range(7)]

        for date in date_range:
            report_filename = f"{date.strftime('%Y-%m-%d')}.md"
            report_path = os.path.join(self.reports_directory, report_filename)

            try:
                if os.path.exists(report_path):
                    with open(report_path, "r", encoding="utf-8") as file:
                        weekly_reports.append(
                            f'{report_filename}\n{file.read()}'
                        )
            except Exception as e:
                print(f"Erro ao ler {report_path}: {e}")

        return "\n\n".join(weekly_reports)

    def generate_weekly_summary(self, end_date=None):
        """
        Gera um resumo semanal usando Ollama.
        """
        if end_date is None:
            today = datetime.now()
            end_date = today - timedelta(days=today.weekday())

        weekly_content = self._get_weekly_reports(end_date)

        prompt = f"""
        Analise os seguintes relatórios diários e gere um resumo
        pequeno e simplificado:
        1. Atividades na semana
        2. Resolução de bugs
        3. Trabalhando em features

        Seja claro e direto, utilize pontos para destacar
        as principais informações importantes.
        Replique o formato de como eu falo nos relatórios.

        Relatórios:
        {weekly_content}
        """

        if Config.DEBUG:
            print("[DEBUG] PROMPT:\n\n" + prompt)

        return self._ai.generate_content(prompt)
