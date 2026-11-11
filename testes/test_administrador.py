
import unittest

from modelos.administrador import Administrador


class CatalogoTeste:
    def __init__(self):
        self.operacao = None
        self.argumentos = None

    def adicionar_livro(self, livro, administrador=None):
        self.operacao = "adicionar"
        self.argumentos = (livro, administrador)

    def remover_livro(self, id_livro, administrador=None):
        self.operacao = "remover"
        self.argumentos = (id_livro, administrador)

    def editar_livro(self, id_livro, administrador=None, **alteracoes):
        self.operacao = "editar"
        self.argumentos = (id_livro, administrador, alteracoes)


class TestAdministrador(unittest.TestCase):
    def setUp(self):
        self.admin = Administrador(
            1, "Administrador", "admin@email.com", "123456"
        )
        self.catalogo = CatalogoTeste()

    def test_tipo(self):
        self.assertEqual(self.admin.tipo(), "administrador")

    def test_adicionar_livro(self):
        livro = "Livro de teste"

        self.admin.adicionar_livro(self.catalogo, livro)

        self.assertEqual(self.catalogo.operacao, "adicionar")
        self.assertEqual(
            self.catalogo.argumentos,
            (livro, self.admin)
        )

    def test_remover_livro(self):
        self.admin.remover_livro(self.catalogo, 1)

        self.assertEqual(self.catalogo.operacao, "remover")
        self.assertEqual(
            self.catalogo.argumentos,
            (1, self.admin)
        )

    def test_editar_livro(self):
        self.admin.editar_livro(
            self.catalogo, 1, titulo="Novo título"
        )

        self.assertEqual(self.catalogo.operacao, "editar")
        self.assertEqual(
            self.catalogo.argumentos,
            (1, self.admin, {"titulo": "Novo título"})
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
