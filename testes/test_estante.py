import unittest
import json
import os
from pathlib import Path

from modelos.livro import Livro
from gestores.catalogo import Catalogo
from gestores.estante import Estante


class BancoTeste:
    def __init__(self):
        caminho = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dados",
    "catalogo.json"
)

        with open(caminho, "r", encoding="utf-8") as arquivo:
            self.livros = json.load(arquivo)

        self.leituras = []

    def carregar_catalogo(self):
        return self.livros.copy()

    def salvar_catalogo(self, dados):
        self.livros = dados.copy()

    def carregar_leituras(self):
        return self.leituras.copy()

    def salvar_leituras(self, dados):
        self.leituras = dados.copy()


class TestEstante(unittest.TestCase):
    def setUp(self):
        self.banco = BancoTeste()
        self.catalogo = Catalogo(self.banco)
        self.estante = Estante(1, self.catalogo, self.banco)

    def test_adicionar_leitura(self):
        self.estante.adicionar_leitura(1)

        leituras = self.estante.listar_todas()

        self.assertEqual(len(leituras), 1)
        self.assertEqual(leituras[0].livro_id, 1)

    def test_impedir_livro_repetido(self):
        self.estante.adicionar_leitura(1)

        with self.assertRaises(ValueError):
            self.estante.adicionar_leitura(1)

    def test_impedir_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.estante.adicionar_leitura(999)

    def test_filtrar_por_status(self):
        self.estante.adicionar_leitura(1, "Lendo")
        self.estante.adicionar_leitura(2, "Quero ler")

        leituras = self.estante.filtrar_por_status("Lendo")

        self.assertEqual(len(leituras), 1)
        self.assertEqual(leituras[0].livro_id, 1)

    def test_favoritar_livro(self):
        self.estante.adicionar_leitura(1)

        resultado = self.estante.alternar_favorito(1)

        self.assertTrue(resultado)
        self.assertEqual(len(self.estante.listar_favoritos()), 1)

    def test_avaliar_livro(self):
        self.estante.adicionar_leitura(1)
        self.estante.avaliar_livro(1, 5)

        leitura = self.estante.buscar_leitura(1)

        self.assertEqual(leitura.avaliacao, 5)

    def test_impedir_avaliacao_invalida(self):
        self.estante.adicionar_leitura(1)

        with self.assertRaises(ValueError):
            self.estante.avaliar_livro(1, 6)

    def test_remover_leitura(self):
        self.estante.adicionar_leitura(1)
        self.estante.remover_leitura(1)

        self.assertEqual(len(self.estante.listar_todas()), 0)

    def test_meta_anual(self):
        self.estante.definir_meta_anual(4)
        self.estante.adicionar_leitura(1)
        self.estante.atualizar_status(1, "Lido")

        progresso = self.estante.calcular_progresso_meta()

        self.assertEqual(progresso, 25)


if __name__ == "__main__":
    unittest.main(verbosity=2)

