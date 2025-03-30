import os
from datetime import datetime

from src.ai.adapters import GeminiAdapter
from src.ai.services import WeeklySummarizer
from src.utils.args_handler import ArgumentParser


def main():
    args_parser = ArgumentParser()
    args = args_parser.parse()

    ai = GeminiAdapter(
        system_instruction=(
            "You are a helpful assistant that summarizes weekly reports "
            "in Portuguese."
        )
    )
    summarizer = WeeklySummarizer(args.reports_dir, ai)

    weekly_summary = summarizer.generate_weekly_summary(args.end_date)

    if weekly_summary:
        file_extension = args.format

        output_file = os.path.join(
            args.output_dir,
            'resumo_semanal_'
            f'{datetime.now().strftime("%Y-%m-%d")}'
            f'.{file_extension}'
        )
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(weekly_summary)

        print(f"[+] Resumo semanal gerado em {output_file}")

    if args.verbose:
        print("[i] Processamento concluído com sucesso.")


if __name__ == "__main__":
    print(
        """
    ██╗    ██╗███████╗███████╗██╗  ██╗██╗  ██╗   ██╗
    ██║    ██║██╔════╝██╔════╝██║ ██╔╝██║  ╚██╗ ██╔╝
    ██║ █╗ ██║█████╗  █████╗  █████╔╝ ██║   ╚████╔╝
    ██║███╗██║██╔══╝  ██╔══╝  ██╔═██╗ ██║    ╚██╔╝
    ╚███╔███╔╝███████╗███████╗██║  ██╗███████╗██║
    ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝
    ██████╗ ███████╗██████╗  ██████╗ ██████╗ ████████╗███████╗
    ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
    ██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝   ██║   ███████╗
    ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
    ██║  ██║███████╗██║     ╚██████╔╝██║  ██║   ██║   ███████║
    ╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝

    Versão 0.1.0

    Um assistente de sumarização de relatórios semanais em português,
    feito com carinho por Ryan Guimarães.
    """
    )
    main()
