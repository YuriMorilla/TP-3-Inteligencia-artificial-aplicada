import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("EDUACESSO_API_CSV", str(tmp_path / "api.csv"))
    return TestClient(app)


NOVO = {
    "municipio": "Aparecida do Taboado", "uf": "ms", "ideb_anos_iniciais": 5.1,
    "ideb_anos_finais": 4.2, "taxa_abandono_pct": 3.0, "escolas_internet_pct": 70,
    "pib_per_capita": 25000, "ano": 2024,
}


def test_raiz(client):
    assert client.get("/").json()["servico"] == "EduAcesso ESG API"


def test_listar_com_filtros(client):
    r = client.get("/municipios", params={"uf": "MS", "ideb_min": 5.0})
    assert r.status_code == 200
    assert {m["municipio"] for m in r.json()} == {"Campo Grande", "Três Lagoas", "Dourados"}
    assert all(m["uf"] == "MS" and m["ideb_anos_iniciais"] >= 5.0 for m in r.json())


def test_consulta_sem_acento_e_404(client):
    assert client.get("/municipios/tres lagoas").json()[0]["uf"] == "MS"
    assert client.get("/municipios/inexistente").status_code == 404


def test_post_persiste_e_aparece_no_get(client):
    r = client.post("/municipios", json=NOVO)
    assert r.status_code == 201 and r.json()["uf"] == "MS"
    assert client.get("/municipios/Aparecida do Taboado").json()[0]["ano"] == 2024
    assert client.post("/municipios", json=NOVO).status_code == 409  # duplicado


def test_post_valida_campos(client):
    ruim = {**NOVO, "ideb_anos_iniciais": 15}
    assert client.post("/municipios", json=ruim).status_code == 422


def test_estatisticas_noticias_corpus(client):
    assert client.get("/estatisticas").json()["total_registros"] >= 15
    assert client.get("/noticias").json()["total"] > 0
    docs = client.get("/corpus", params={"tipo": "noticia"}).json()["documentos"]
    assert docs and all(d["tipo"] == "noticia" for d in docs)
