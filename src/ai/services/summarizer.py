import os
from datetime import datetime, timedelta

from src.ai.adapters.base import AIAdapter
from src.config.settings import Config


class WeeklySummarizer:

    __slots__ = ["reports_directory", "_ai"]

    def __init__(self, reports_directory, ai: AIAdapter = None):
        self.reports_directory = reports_directory
        self._ai = ai

    def _get_weekly_reports(self, start_date, end_date):
        """
        Coleta todos os relatórios de uma semana específica.
        Formato dos arquivos: YYYY-MM-DD.md em uma única pasta.
        """
        weekly_reports = []

        date_range = [
            start_date + timedelta(days=x)
            for x in range((end_date - start_date).days + 1)
        ]

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

    def generate_weekly_summary(self, start_date=None, end_date=None):
        """
        Generates a summary of a week of reports.
        """
        if not start_date:
            start_date = self._get_last_week_start()
        if not end_date:
            end_date = self._get_last_week_end()

        weekly_content = self._get_weekly_reports(start_date, end_date)

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

    def _get_last_week_start(self):
        """
        Returns the start of last week (Sunday)
        """
        last_week = datetime.now() - timedelta(days=7)
        last_week_sunday = last_week - timedelta(days=last_week.weekday() + 1)
        return last_week_sunday

    def _get_last_week_end(self):
        """
        Returns the end of last week (Saturday)
        """
        last_week_start = self._get_last_week_start()
        return last_week_start + timedelta(days=6)
