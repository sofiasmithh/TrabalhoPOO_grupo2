
import unittest
import json
import os
from pathlib import Path

from modelos.livro import Livro
from gestores.catalogo import Catalogo


class BancoTeste:
    def __init__(self):
        caminho = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dados",
    "catalogo.json"
)

        with open(caminho, "r", encoding="utf-8") as arquivo:
            self.livros = json.load(arquivo)

    def carregar_catalogo(self):
        return self.livros.copy()

    def salvar_catalogo(self, dados):
        self.livros = dados.copy()


class AdministradorTeste:
    def tipo(self):
        return "administrador"


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.banco = BancoTeste()
        self.catalogo = Catalogo(self.banco)
        self.admin = AdministradorTeste()

    def test_carregar_livros(self):
        self.assertEqual(len(self.catalogo.listar_livros()), 5)

    def test_buscar_por_id(self):
        livro = self.catalogo.buscar_por_id(1)

        self.assertIsNotNone(livro)
        self.assertEqual(livro.titulo, "Dom Casmurro")

    def test_buscar_por_titulo(self):
        livros = self.catalogo.buscar_por_titulo("hobbit")

        self.assertEqual(len(livros), 1)
        self.assertEqual(livros[0].titulo, "O Hobbit")

    def test_adicionar_livro(self):
        livro = Livro(
            6, "Capitaes da Areia", "Jorge Amado",
            "Romance", 1937, 280
        )

        self.catalogo.adicionar_livro(livro, self.admin)

        self.assertIsNotNone(self.catalogo.buscar_por_id(6))

    def test_impedir_id_repetido(self):
        livro = Livro(
            1, "Outro Livro", "Autor",
            "Romance", 2020, 100
        )

        with self.assertRaises(ValueError):
            self.catalogo.adicionar_livro(livro, self.admin)

    def test_impedir_alteracao_sem_admin(self):
        livro = Livro(
            6, "Livro Novo", "Autor",
            "Romance", 2020, 100
        )

        with self.assertRaises(PermissionError):
            self.catalogo.adicionar_livro(livro)

    def test_editar_livro(self):
        self.catalogo.editar_livro(
            1, self.admin, titulo="Dom Casmurro Editado"
        )

        livro = self.catalogo.buscar_por_id(1)

        self.assertEqual(livro.titulo, "Dom Casmurro Editado")

    def test_remover_livro(self):
        self.catalogo.remover_livro(1, self.admin)

        self.assertIsNone(self.catalogo.buscar_por_id(1))


if __name__ == "__main__":
    unittest.main(verbosity=2)

