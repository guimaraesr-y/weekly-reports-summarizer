import pytest
from datetime import datetime, timedelta


@pytest.fixture
def sample_report_content():
    """Fixture that provides sample report content for testing."""
    return """
    # Relatório Diário - 2024-03-28

    ## Atividades Realizadas
    - Implementação de novas features
    - Correção de bugs
    - Reunião de planejamento

    ## Próximos Passos
    - Continuar desenvolvimento
    - Revisar código
    - Preparar apresentação
    """


@pytest.fixture
def sample_reports_dir(tmp_path, sample_report_content):
    """Fixture that creates a temporary directory with sample reports."""
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()

    last_week = datetime.now() - timedelta(days=7)
    last_week_monday = last_week - timedelta(days=last_week.weekday())

    # Create sample reports for a week
    for i in range(4):
        date = last_week_monday + timedelta(days=i)
        report_file = reports_dir / f"{date.strftime('%Y-%m-%d')}.md"
        report_file.write_text(sample_report_content)

    return str(reports_dir)
