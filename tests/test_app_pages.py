"""Smoke tests: cada página do app executa sem exceções."""
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

VIEWS = ["home", "indicadores", "noticias", "dados", "api", "llm"]


@pytest.mark.parametrize("view", VIEWS)
def test_view_roda_sem_erro(view):
    at = AppTest.from_file(str(APP_DIR / "views" / f"{view}.py"), default_timeout=30).run()
    assert not at.exception, [e.value for e in at.exception]


def test_entrypoint_com_navegacao():
    at = AppTest.from_file(str(APP_DIR / "main.py"), default_timeout=30).run()
    assert not at.exception, [e.value for e in at.exception]


def test_filtro_indicadores_reduz_selecao():
    at = AppTest.from_file(str(APP_DIR / "views" / "indicadores.py"), default_timeout=30).run()
    at.multiselect(key="uf_filter").set_value(["MS"]).run()
    assert not at.exception
    assert at.metric[0].value == "5"  # Campo Grande, Três Lagoas, Dourados, Corumbá, Ponta Porã
